"""
LangChain-Powered Requirement Analyst Backend
Uses: gemini-flash-lite-latest via LangChain
Server: Built-in Python HTTP server (avoids Pydantic V1/V2 crash on Python 3.14)
"""
import os
import sys
import json
import warnings
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv

# Suppress the Pydantic V1 warning on Python 3.14
warnings.filterwarnings("ignore", category=UserWarning)

# LangChain Imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load .env from the same directory as this script
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("ERROR: GOOGLE_API_KEY not found in .env file!")
    sys.exit(1)

print(f"[OK] API Key loaded: {api_key[:10]}...")

# Initialize LangChain Model
llm = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest", temperature=0.2)
print("[OK] LangChain LLM initialized successfully.")

# =============================================
# LangChain Chains
# =============================================
clarify_prompt = PromptTemplate(
    input_variables=["segment"],
    template="""You are an expert AI Requirement Analyst participating in a live software requirement meeting.
Analyze this transcript segment: "{segment}"

Does this segment contain a software requirement that is vague, incomplete, or ambiguous?
If YES, output a SINGLE, short, direct clarification question to ask the stakeholder. 
If NO (it's clear, or just general chat), output exactly the word "NONE".

Do not provide explanations. Output either the question or "NONE"."""
)
clarify_chain = clarify_prompt | llm | StrOutputParser()

requirements_prompt = PromptTemplate(
    input_variables=["transcript", "qna_text"],
    template="""You are a Senior Systems Analyst. Based on the following live meeting transcript and the subsequent clarification Q&A, generate refined software requirements.

RAW TRANSCRIPT:
{transcript}

CLARIFICATION Q&A:
{qna_text}

INSTRUCTIONS:
Generate a structured JSON output containing:
1. "FRs": An array of refined Functional Requirements (strings).
2. "NFRs": An array of objects with "category" (e.g., Security, Performance, Fairness) and "description" for Non-Functional Requirements.
3. "Comparison": A short text evaluating how the clarification questions improved the requirements (Before vs After).
4. "QualityScore": A score from 1-10 on the final quality.

Output ONLY valid JSON with no markdown formatting. No extra text before or after the JSON."""
)
requirements_chain = requirements_prompt | llm | StrOutputParser()

print("[OK] LangChain Chains created.")

# =============================================
# HTTP Server
# =============================================
class RequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/" or self.path == "":
            self._send_json(200, {"message": "LangChain Requirement Analyst Backend is running!"})
        else:
            self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)
        
        try:
            body = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Invalid JSON body"})
            return

        if self.path == "/api/clarify":
            self._handle_clarify(body)
        elif self.path == "/api/generate_requirements":
            self._handle_generate(body)
        else:
            self._send_json(404, {"error": "Not found"})

    def _handle_clarify(self, body):
        text = body.get("text", "")
        if not text.strip():
            self._send_json(400, {"error": "text field is required"})
            return

        try:
            print(f"[CLARIFY] Processing: {text[:80]}...")
            result = clarify_chain.invoke({"segment": text})
            print(f"[CLARIFY] Result: {result.strip()}")
            self._send_json(200, {"result": result.strip()})
        except Exception as e:
            print(f"[CLARIFY ERROR] {e}")
            self._send_json(500, {"error": str(e)})

    def _handle_generate(self, body):
        transcript = body.get("transcript", "")
        questions = body.get("questions", [])

        qna_text = ""
        for q in questions:
            qna_text += f"Q: {q.get('question','')}\nA: {q.get('answer','')}\n\n"

        if not qna_text.strip():
            qna_text = "No clarification questions were asked."

        try:
            print(f"[GENERATE] Processing transcript ({len(transcript)} chars)...")
            ai_response = requirements_chain.invoke({
                "transcript": transcript,
                "qna_text": qna_text
            })
            # Clean up potential markdown
            ai_response = ai_response.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(ai_response)
            print(f"[GENERATE] Success! FRs: {len(parsed.get('FRs', []))}, NFRs: {len(parsed.get('NFRs', []))}")
            self._send_json(200, parsed)
        except json.JSONDecodeError:
            print(f"[GENERATE] JSON parse failed. Raw: {ai_response[:200]}")
            self._send_json(500, {"error": "AI returned invalid JSON", "raw": ai_response[:500]})
        except Exception as e:
            print(f"[GENERATE ERROR] {e}")
            self._send_json(500, {"error": str(e)})

    def log_message(self, format, *args):
        """Override to show cleaner logs"""
        print(f"[HTTP] {args[0]}")


def main():
    port = 8000
    server = HTTPServer(("127.0.0.1", port), RequestHandler)
    print(f"\n{'='*50}")
    print(f" LangChain Backend running on http://127.0.0.1:{port}")
    print(f" Endpoints:")
    print(f"   POST /api/clarify           - Real-time clarification")
    print(f"   POST /api/generate_requirements - Full requirement generation")
    print(f"{'='*50}\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
