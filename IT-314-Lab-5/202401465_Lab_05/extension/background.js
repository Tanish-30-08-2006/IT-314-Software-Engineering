/*
  Background Service Worker
  Routes messages between the content script / popup and the Python LangChain backend.
*/

const BACKEND_URL = "http://127.0.0.1:8000/api";

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {

    // ---- FAST CLARIFICATION LOOP ----
    if (request.action === "process_transcript") {
        const segment = request.text;
        console.log("[BG] Sending to /api/clarify:", segment);

        fetch(`${BACKEND_URL}/clarify`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: segment })
        })
        .then(res => {
            if (!res.ok) throw new Error("Backend returned " + res.status);
            return res.json();
        })
        .then(data => {
            const answer = (data.result || "").trim();
            console.log("[BG] Clarify result:", answer);

            if (answer && answer.toUpperCase() !== "NONE") {
                // Store the question
                chrome.storage.local.get(["clarificationQuestions"], (resLocal) => {
                    let questions = resLocal.clarificationQuestions || [];
                    questions.push({
                        id: Date.now(),
                        transcriptContext: segment,
                        question: answer,
                        stakeholderResponse: null
                    });
                    chrome.storage.local.set({ clarificationQuestions: questions }, () => {
                        // Notify the popup to refresh
                        chrome.runtime.sendMessage({ action: "new_question_available" }).catch(() => {});
                    });
                });
            }
        })
        .catch(err => {
            console.error("[BG] Clarify error:", err.message);
        });

        // Don't block
        return false;
    }

    // ---- DEEP REQUIREMENTS GENERATION ----
    if (request.action === "generate_requirements") {
        chrome.storage.local.get(["transcriptHistory", "clarificationQuestions"], (resLocal) => {
            const transcript = resLocal.transcriptHistory || "";
            const questions = resLocal.clarificationQuestions || [];

            const payloadQuestions = questions
                .filter(q => q.stakeholderResponse)
                .map(q => ({ question: q.question, answer: q.stakeholderResponse }));

            console.log("[BG] Sending to /api/generate_requirements...");

            fetch(`${BACKEND_URL}/generate_requirements`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    transcript: transcript,
                    questions: payloadQuestions
                })
            })
            .then(res => {
                if (!res.ok) throw new Error("Backend returned " + res.status);
                return res.json();
            })
            .then(data => {
                console.log("[BG] Requirements generated:", data);
                sendResponse({ success: true, data: data });
            })
            .catch(err => {
                console.error("[BG] Generate error:", err.message);
                sendResponse({ success: false, error: "Backend error: " + err.message + ". Is the Python server running?" });
            });
        });

        return true; // Keep channel open for async sendResponse
    }

    // ---- SIMULATE (from popup when NOT on a Google Meet page) ----
    if (request.action === "simulate_from_popup") {
        const text = request.text;
        console.log("[BG] Simulating from popup:", text);

        // Store transcript
        chrome.storage.local.get(["transcriptHistory"], (resLocal) => {
            let history = resLocal.transcriptHistory || "";
            history += text + "\n";
            chrome.storage.local.set({ transcriptHistory: history });
        });

        // Send to clarify endpoint
        fetch(`${BACKEND_URL}/clarify`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text })
        })
        .then(res => {
            if (!res.ok) throw new Error("Backend returned " + res.status);
            return res.json();
        })
        .then(data => {
            const answer = (data.result || "").trim();
            console.log("[BG] Simulate clarify result:", answer);

            if (answer && answer.toUpperCase() !== "NONE") {
                chrome.storage.local.get(["clarificationQuestions"], (resLocal) => {
                    let questions = resLocal.clarificationQuestions || [];
                    questions.push({
                        id: Date.now(),
                        transcriptContext: text,
                        question: answer,
                        stakeholderResponse: null
                    });
                    chrome.storage.local.set({ clarificationQuestions: questions }, () => {
                        chrome.runtime.sendMessage({ action: "new_question_available" }).catch(() => {});
                        sendResponse({ status: "ok", question: answer });
                    });
                });
            } else {
                sendResponse({ status: "ok", question: null });
            }
        })
        .catch(err => {
            console.error("[BG] Simulate error:", err.message);
            sendResponse({ status: "error", error: err.message });
        });

        return true; // async
    }
});
