const BACKEND = "http://127.0.0.1:8000";

// =============================================
// Tab Switching
// =============================================
document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", e => {
        document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
        document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
        e.target.classList.add("active");
        document.getElementById(e.target.getAttribute("data-tab")).classList.add("active");
    });
});

// =============================================
// Backend Health Check on Popup Open
// =============================================
async function checkBackend() {
    const bar = document.getElementById("statusBar");
    try {
        const res = await fetch(BACKEND + "/", { method: "GET" });
        if (res.ok) {
            bar.textContent = "✅ Backend connected (LangChain + gemini-flash-lite)";
            bar.className = "status-bar status-ok";
        } else {
            bar.textContent = "❌ Backend returned error " + res.status;
            bar.className = "status-bar status-error";
        }
    } catch (e) {
        bar.textContent = "❌ Cannot connect to backend. Run: python app.py";
        bar.className = "status-bar status-error";
    }
}

// =============================================
// Load & Display Questions
// =============================================
function loadQuestions() {
    chrome.storage.local.get(["clarificationQuestions"], res => {
        const container = document.getElementById("questionsContainer");
        const questions = res.clarificationQuestions || [];

        if (questions.length === 0) {
            container.innerHTML = '<p class="empty-state">No ambiguous requirements detected yet.</p>';
            return;
        }

        container.innerHTML = "";
        questions.forEach(q => {
            const card = document.createElement("div");
            card.className = "question-card";

            const escapedContext = q.transcriptContext.replace(/</g, "&lt;").replace(/>/g, "&gt;");
            const escapedQuestion = q.question.replace(/</g, "&lt;").replace(/>/g, "&gt;");
            const escapedResponse = (q.stakeholderResponse || "").replace(/</g, "&lt;").replace(/>/g, "&gt;");

            card.innerHTML = `
                <div class="context">"${escapedContext}"</div>
                <div class="q-text">🤖 ${escapedQuestion}</div>
                <textarea id="ans-${q.id}" rows="2" placeholder="Type the stakeholder's response..."
                    ${q.stakeholderResponse ? "disabled" : ""}>${escapedResponse}</textarea>
                ${!q.stakeholderResponse
                    ? `<button class="save-ans-btn" data-id="${q.id}">Save Answer</button>`
                    : '<span style="color:#1e8e3e;font-size:12px;">✅ Answered</span>'}
            `;
            container.appendChild(card);
        });

        // Attach save handlers
        document.querySelectorAll(".save-ans-btn").forEach(btn => {
            btn.addEventListener("click", e => {
                const id = parseInt(e.target.getAttribute("data-id"));
                const textarea = document.getElementById("ans-" + id);
                const answer = textarea ? textarea.value : "";
                if (!answer.trim()) return;

                chrome.storage.local.get(["clarificationQuestions"], res2 => {
                    let qs = res2.clarificationQuestions || [];
                    const idx = qs.findIndex(item => item.id === id);
                    if (idx > -1) {
                        qs[idx].stakeholderResponse = answer;
                        chrome.storage.local.set({ clarificationQuestions: qs }, loadQuestions);
                    }
                });
            });
        });
    });
}

// =============================================
// Simulate (sends DIRECTLY to backend from popup)
// =============================================
document.getElementById("simulateBtn").addEventListener("click", async () => {
    const textArea = document.getElementById("simulateText");
    const resultDiv = document.getElementById("simulateResult");
    const text = textArea.value.trim();

    if (!text) {
        resultDiv.innerHTML = '<span style="color:red;">Please enter some text first.</span>';
        return;
    }

    const btn = document.getElementById("simulateBtn");
    btn.disabled = true;
    btn.textContent = "Analyzing...";
    resultDiv.innerHTML = '<span style="color:#b06000;">⏳ Sending to LangChain backend...</span>';

    try {
        // Store transcript locally
        const stored = await chrome.storage.local.get(["transcriptHistory"]);
        let history = stored.transcriptHistory || "";
        history += text + "\n";
        await chrome.storage.local.set({ transcriptHistory: history });

        // Call backend directly from popup (no content script needed)
        const res = await fetch(BACKEND + "/api/clarify", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text })
        });

        if (!res.ok) {
            const errData = await res.text();
            throw new Error("HTTP " + res.status + ": " + errData);
        }

        const data = await res.json();
        const answer = (data.result || "").trim();

        if (answer.toUpperCase() === "NONE") {
            resultDiv.innerHTML = '<span style="color:#1e8e3e;">✅ Statement is clear. No clarification needed.</span>';
        } else {
            // Store the question
            const qStored = await chrome.storage.local.get(["clarificationQuestions"]);
            let questions = qStored.clarificationQuestions || [];
            questions.push({
                id: Date.now(),
                transcriptContext: text,
                question: answer,
                stakeholderResponse: null
            });
            await chrome.storage.local.set({ clarificationQuestions: questions });

            resultDiv.innerHTML = `<span style="color:#1a73e8;">🤖 Question generated! Check the <b>Live Q&A</b> tab.</span>`;
            loadQuestions(); // Refresh the live tab
        }

        textArea.value = "";
    } catch (err) {
        resultDiv.innerHTML = `<span style="color:red;">❌ Error: ${err.message}<br>Make sure the Python backend is running.</span>`;
    } finally {
        btn.disabled = false;
        btn.textContent = "Simulate Transcript Segment";
    }
});

// =============================================
// Generate Requirements
// =============================================
document.getElementById("generateBtn").addEventListener("click", () => {
    const btn = document.getElementById("generateBtn");
    btn.textContent = "Generating... (10-20s)";
    btn.disabled = true;

    chrome.runtime.sendMessage({ action: "generate_requirements" }, response => {
        btn.textContent = "Generate Requirements";
        btn.disabled = false;

        if (response && response.success) {
            renderDashboard(response.data);
            document.querySelector('[data-tab="dashboard-tab"]').click();
        } else {
            const errMsg = (response && response.error) || "Failed. Is the Python server running?";
            alert(errMsg);
        }
    });
});

// =============================================
// Clear All Data
// =============================================
document.getElementById("clearBtn").addEventListener("click", () => {
    chrome.storage.local.remove(["transcriptHistory", "clarificationQuestions"], () => {
        loadQuestions();
        document.getElementById("dashboardContent").innerHTML = '<p class="empty-state">Data cleared.</p>';
        document.getElementById("exportActions").style.display = "none";
    });
});

// =============================================
// Dashboard Renderer
// =============================================
let currentRequirementsData = null;

function renderDashboard(data) {
    currentRequirementsData = data;
    const content = document.getElementById("dashboardContent");
    document.getElementById("exportActions").style.display = "flex";

    let html = `
        <div class="req-section">
            <h4>Quality Evaluation</h4>
            <p><strong>Score:</strong> ${data.QualityScore || "N/A"} / 10</p>
            <p><strong>Impact of Clarification:</strong> ${data.Comparison || "N/A"}</p>
        </div>
        <div class="req-section">
            <h4>Functional Requirements (FRs)</h4>
    `;

    if (Array.isArray(data.FRs)) {
        data.FRs.forEach(fr => { html += `<div class="req-item">${fr}</div>`; });
    } else {
        html += `<p>${data.FRs || "None generated"}</p>`;
    }

    html += `</div><div class="req-section"><h4>Non-Functional Requirements (NFRs)</h4>`;

    if (Array.isArray(data.NFRs)) {
        data.NFRs.forEach(nfr => {
            html += `<div class="req-item"><strong>${nfr.category || ""}:</strong> ${nfr.description || ""}</div>`;
        });
    } else {
        html += `<p>${data.NFRs || "None generated"}</p>`;
    }

    html += `</div>`;
    content.innerHTML = html;
}

// =============================================
// Export to TXT
// =============================================
document.getElementById("exportTxtBtn").addEventListener("click", () => {
    if (!currentRequirementsData) return;
    const d = currentRequirementsData;
    let txt = "AI Requirement Analysis Report\n================================\n\n";
    txt += "Quality Score: " + (d.QualityScore || "N/A") + "/10\n";
    txt += "Comparison: " + (d.Comparison || "N/A") + "\n\n";
    txt += "Functional Requirements:\n";
    if (Array.isArray(d.FRs)) {
        d.FRs.forEach(fr => { txt += "- " + fr + "\n"; });
    }
    txt += "\nNon-Functional Requirements:\n";
    if (Array.isArray(d.NFRs)) {
        d.NFRs.forEach(nfr => { txt += "- [" + (nfr.category || "") + "] " + (nfr.description || "") + "\n"; });
    }

    const blob = new Blob([txt], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "requirements.txt";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
});

// =============================================
// Listen for new questions from background
// =============================================
chrome.runtime.onMessage.addListener((request) => {
    if (request.action === "new_question_available") {
        loadQuestions();
    }
});

// =============================================
// INIT
// =============================================
checkBackend();
loadQuestions();
