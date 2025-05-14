document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");

    
    function addMessage(sender, content) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender);

        if (sender === "agent" && typeof content === "object" && content.plot_url) {
            // If agent sends a plot URL, display text and image
            if (content.text) {
                const textSpan = document.createElement("span");
                textSpan.textContent = content.text;
                messageDiv.appendChild(textSpan);
            }
            const img = document.createElement("img");
            img.src = content.plot_url;
            img.alt = "Weather Plot";
            img.style.maxWidth = "100%"; // Optional: for basic styling
            img.style.marginTop = "10px"; // Optional: for basic styling
            messageDiv.appendChild(img);
        } else if (sender === "agent" && typeof content === "object" && content.text) {
            // If agent sends only text
            messageDiv.textContent = content.text;
        }
         else {
            // For user messages or simple agent text messages
            messageDiv.textContent = content;
        }

        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    
    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessage("user", message);
        userInput.value = "";

        
        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message }),
            });
            const data = await response.json();
            if (data.response) {
                // Pass the whole data.response object which might contain text and plot_url
                addMessage("agent", data.response);
            } else {
                addMessage("agent", "[Error: No response from agent]");
            }
        } catch (error) {
            addMessage("agent", "[Error: Failed to connect to server]");
        }
    }

    
    sendButton.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendMessage();
    });
});