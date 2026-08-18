import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ==========================================
# Setup and Initialization
# ==========================================
# Load environment variables from .env file (Make sure GOOGLE_API_KEY is present)
load_dotenv()

# Ensure the Google API key is available
if "GOOGLE_API_KEY" not in os.environ:
    raise ValueError("Please set GOOGLE_API_KEY in your .env file")

# Initialize the LLM using LangChain and Google GenAI
# We use gemini-flash-lite-latest to ensure compatibility with modern endpoints and speed
llm = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest", temperature=0.4, max_retries=10)


# ==========================================
# Human-in-the-Loop (HITL) Feedback Function
# ==========================================
def run_stage_with_feedback(prompt_template, input_variables, stage_name):
    """
    Executes a LangChain prompt, displays the output to the user, and enters a feedback loop.
    If the user provides feedback, the LLM is prompted to refine the output.
    If the user presses Enter without typing anything, the output is approved and returned.
    """
    print(f"\n Running {stage_name}...")
    
    # Create the chain using LCEL with a string parser to automatically parse the AIMessage
    chain = prompt_template | llm | StrOutputParser()
    
    # Generate initial AI output as a pure string
    current_output = chain.invoke(input_variables)
    
    # Feedback Loop (Mandatory Design Requirement for the Lab)
    while True:
        print(f"\n{'='*60}")
        print(f"--- OUTPUT: {stage_name} ---")
        print(current_output)
        print(f"{'='*60}\n")
        
        # Ask the human reviewer for input
        feedback = input("📝 Reviewer Feedback (Press Enter to approve, or type changes to refine): ").strip()
        
        if not feedback:
            # If input is empty, the user approved the output
            print(f"✅ {stage_name} Approved!\n")
            break
        
        print("\n⏳ Refining based on your feedback...")
        
        # Refinement Prompt to steer the LLM using the human feedback
        refine_template = """
        You are an expert Requirements Engineer. 
        Here is your previous output:
        {original_output}
        
        The human reviewer provided the following feedback/corrections:
        {feedback}
        
        Please revise and improve the output based strictly on the feedback provided.
        """
        refine_prompt = PromptTemplate(
            input_variables=["original_output", "feedback"],
            template=refine_template
        )
        
        refine_chain = refine_prompt | llm | StrOutputParser()
        
        # Generate refined output
        current_output = refine_chain.invoke({
            "original_output": current_output,
            "feedback": feedback
        })

    return current_output


# ==========================================
# Main Execution Pipeline
# ==========================================
def main():
    # Step 0: Input Case Study Ingestion
    # We define the raw narrative of the Smart Campus Cafeteria system here.
    case_study = """
    Smart Campus Cafeteria / Food Court Ordering & Feedback System
    Most college campuses run their cafeterias manually: students wait in unpredictably long queues, place orders verbally, and wait again without knowing prep time. This causes overcrowding and frustration. Cash/card handling is slow, and manual errors are common.
    Vendors manage inventory manually, leading to food wastage or stock-outs. Feedback is informal (word of mouth).
    Administration wants to oversee pricing, hygiene, and value without relying solely on manual inspections. Hostel wardens also track meal plans for hostel students.
    The new system should allow digital ordering, real-time tracking, inventory/sales management for vendors, and a structured feedback loop. It should also give admin and wardens oversight tools.
    """
    
    print(" Starting Automated Requirements Elicitation Pipeline...")

    # ---------------------------------------------------------
    # Step 1: Stakeholder Identification
    # ---------------------------------------------------------
    prompt_stage_1 = PromptTemplate(
        input_variables=["case_study"],
        template="""
        Analyze the following case study and identify all primary, secondary, and administrative stakeholders.
        Provide a structured list of roles with a brief 1-sentence justification for each.
        
        Case Study:
        {case_study}
        """
    )
    stakeholders = run_stage_with_feedback(prompt_stage_1, {"case_study": case_study}, "Step 1: Stakeholder Identification")


    # ---------------------------------------------------------
    # Step 2: Stakeholder Goals Identification
    # ---------------------------------------------------------
    prompt_stage_2 = PromptTemplate(
        input_variables=["case_study", "stakeholders"],
        template="""
        Based on the case study and the identified stakeholders, map out the explicit pain points and desired outcomes (goals) for each stakeholder group.
        
        Case Study: {case_study}
        Stakeholders: {stakeholders}
        
        Provide a structured breakdown for each stakeholder group.
        """
    )
    goals = run_stage_with_feedback(prompt_stage_2, {"case_study": case_study, "stakeholders": stakeholders}, "Step 2: Stakeholder Goals Identification")


    # ---------------------------------------------------------
    # Step 3: Elicitation Technique Selection
    # ---------------------------------------------------------
    prompt_stage_3 = PromptTemplate(
        input_variables=["stakeholders", "goals"],
        template="""
        Based on the stakeholders and their goals, select the optimal requirements elicitation technique for each group (e.g., Questionnaires/Surveys, Semi-structured Interviews, Audits, Observations).
        Justify your pairing based on group size, accessibility, and depth of needed insights.
        
        Stakeholders & Goals:
        {goals}
        """
    )
    techniques = run_stage_with_feedback(prompt_stage_3, {"stakeholders": stakeholders, "goals": goals}, "Step 3: Elicitation Technique Selection")


    # ---------------------------------------------------------
    # Step 4: Elicitation Execution
    # ---------------------------------------------------------
    prompt_stage_4 = PromptTemplate(
        input_variables=["techniques"],
        template="""
        Execute the selected elicitation techniques by generating the actual instruments.
        For example, if surveys were chosen for students, draft 4-5 key survey questions. If interviews were chosen for cafeteria vendors, draft 4-5 specific interview questions. Include admin oversight questions if applicable.
        
        Techniques Selected:
        {techniques}
        """
    )
    instruments = run_stage_with_feedback(prompt_stage_4, {"techniques": techniques}, "Step 4: Elicitation Execution")


    # ---------------------------------------------------------
    # Step 5: FR and NFR Generation
    # ---------------------------------------------------------
    prompt_stage_5 = PromptTemplate(
        input_variables=["case_study", "instruments"],
        template="""
        Synthesize all the gathered data, case study, and elicitation instruments to compile the final system requirements.
        Output two structured lists:
        1. Functional Requirements (FRs): Core system features and behaviors (e.g., User Auth, Digital Menu, Tracking).
        2. Non-Functional Requirements (NFRs): Quality attributes (e.g., Peak load handling, Data security, UI usability).
        
        Case Study: {case_study}
        Elicitation Data: {instruments}
        """
    )
    requirements = run_stage_with_feedback(prompt_stage_5, {"case_study": case_study, "instruments": instruments}, "Step 5: FR and NFR Generation")


    # ---------------------------------------------------------
    # Final Step: Exporting the Document
    # ---------------------------------------------------------
    print("\n Pipeline Completed Successfully!")
    output_filename = "final_requirements.txt"
    print(f" Saving final structured document to '{output_filename}'...")
    
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("=== Smart Campus Cafeteria Requirements ===\n\n")
        f.write("--- STAKEHOLDERS ---\n")
        f.write(stakeholders + "\n\n")
        f.write("--- GOALS & PAIN POINTS ---\n")
        f.write(goals + "\n\n")
        f.write("--- ELICITATION TECHNIQUES ---\n")
        f.write(techniques + "\n\n")
        f.write("--- ELICITATION INSTRUMENTS ---\n")
        f.write(instruments + "\n\n")
        f.write("--- FINAL FRs AND NFRs ---\n")
        f.write(requirements + "\n")
        
    print(" Done! You can check 'final_requirements.txt' for the complete generated report.")

if __name__ == "__main__":
    main()
