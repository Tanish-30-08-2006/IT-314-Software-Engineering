/*
  Content Script - Injected into Google Meet pages.
  Monitors the DOM for live captions.
*/

// Let the user know the script actually loaded!
console.log("[LiveReq] Content script loaded. Watching for captions...");
// Temporary alert to confirm the extension is injected into the page.
// If the user doesn't see this when they refresh Google Meet, the extension isn't loaded properly.
alert("LiveReq Analyst Extension is now active on Google Meet!\n\nPlease turn on 'CC' (Captions) at the bottom of the screen and speak to test.");

let currentSentence = "";
let debounceTimer = null;

function sendToBackground(text) {
    if (!text || text.trim().length === 0) return;
    console.log("[LiveReq] Sending segment to background:", text);
    chrome.runtime.sendMessage({ action: "process_transcript", text: text.trim() });
    
    // Store in history
    chrome.storage.local.get(["transcriptHistory"], (res) => {
        let history = res.transcriptHistory || "";
        history += text.trim() + "\n";
        chrome.storage.local.set({ transcriptHistory: history });
    });
}

// Observe the entire document body for any changes
const observer = new MutationObserver((mutations) => {
    let foundNewText = false;

    for (const mutation of mutations) {
        // We look at added nodes
        if (mutation.type === "childList" && mutation.addedNodes.length > 0) {
            for (const node of mutation.addedNodes) {
                // If it's a text node directly, check its parent
                if (node.nodeType === 3) {
                    if (node.textContent && node.textContent.trim().length > 0) {
                        const parent = node.parentElement;
                        const pClass = (parent && parent.className && typeof parent.className === "string") ? parent.className.toLowerCase() : "";
                        // Meet captions usually live inside spans or divs with these classes
                        if (pClass.includes("caption") || pClass.includes("ittpob") || pClass.includes("cnusmb") || pClass.includes("tbmur") || pClass.includes("vbksue")) {
                            currentSentence += node.textContent + " ";
                            foundNewText = true;
                        }
                    }
                    continue;
                }
                
                // If it's an element node
                if (node.nodeType === 1) {
                    const text = node.innerText || node.textContent || "";
                    if (!text.trim()) continue;

                    const cls = (node.className && typeof node.className === "string") ? node.className.toLowerCase() : "";
                    const jsname = node.getAttribute ? node.getAttribute("jsname") : "";

                    const isCaption = 
                        cls.includes("caption") || cls.includes("ittpob") || cls.includes("cnusmb") || 
                        cls.includes("tbmur") || cls.includes("vbksue") || cls.includes("bj4p3b") ||
                        jsname === "YpffJf" || jsname === "tgaKEf";

                    if (isCaption) {
                        currentSentence += text + " ";
                        foundNewText = true;
                    } else {
                        // Check its children just in case
                        const children = node.querySelectorAll ? node.querySelectorAll("span, div") : [];
                        for (const child of children) {
                            const cCls = (child.className && typeof child.className === "string") ? child.className.toLowerCase() : "";
                            const cJsname = child.getAttribute ? child.getAttribute("jsname") : "";
                            if (cCls.includes("caption") || cCls.includes("ittpob") || cCls.includes("cnusmb") || cCls.includes("tbmur") || cCls.includes("vbksue") || cJsname === "YpffJf") {
                                const childText = child.innerText || child.textContent || "";
                                if (childText.trim() && !currentSentence.includes(childText.trim())) {
                                    currentSentence += childText + " ";
                                    foundNewText = true;
                                }
                            }
                        }
                    }
                }
            }
        }
        
        // Also observe if text is updated directly (Google Meet does this often as speech recognition gains confidence)
        if (mutation.type === "characterData") {
            const parent = mutation.target.parentElement;
            const pClass = (parent && parent.className && typeof parent.className === "string") ? parent.className.toLowerCase() : "";
            if (pClass.includes("caption") || pClass.includes("ittpob") || pClass.includes("cnusmb") || pClass.includes("tbmur") || pClass.includes("vbksue")) {
                const text = mutation.target.textContent || "";
                if (text.trim() && !currentSentence.includes(text.trim())) {
                    currentSentence += text + " ";
                    foundNewText = true;
                }
            }
        }
    }

    if (foundNewText) {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            if (currentSentence.trim().length > 0) {
                // Deduplicate repetitive words if Google Meet updates the same span
                // Just send the whole chunk
                sendToBackground(currentSentence.trim());
                currentSentence = ""; // Reset for next sentence
            }
        }, 2000); // Wait 2 seconds of silence before sending the chunk
    }
});

// Configure observer to catch child additions and text updates deeply
observer.observe(document.body, { childList: true, subtree: true, characterData: true });

// Listen for simulation commands
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "simulate_transcript") {
        sendToBackground(request.text);
        sendResponse({ status: "ok" });
    }
    return true;
});
