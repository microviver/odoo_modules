/** @odoo-module **/

document.addEventListener("DOMContentLoaded", () => {
    const chatbotBox = document.createElement("div");
    chatbotBox.id = "chatbot-box";
    chatbotBox.innerHTML = `
        <div id="chatbot-header">Simbi 🤖</div>
        <div id="chatbot-messages"></div>
        <div id="chatbot-typing"><em>piensando...</em></div>
        <input type="text" id="chatbot-input" placeholder="Escreve algo..." />
    `;
    document.body.appendChild(chatbotBox);

    const typing = document.getElementById("chatbot-typing");
    const input = document.getElementById("chatbot-input");
    const messages = document.getElementById("chatbot-messages");

    typing.style.display = "none";

    input.addEventListener("keypress", (e) => {
        if (e.key !== "Enter") return;

        const question = input.value.trim();
        if (!question) return;

        appendMessage(question, "user-msg");
        input.value = "";
        typing.style.display = "block";

        fetch("/ai_chatbot/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question }),
        })
            .then((res) => res.json())
            .then((data) => {
                typing.style.display = "none";
                const answer = data.answer || `Erro: ${data.error}`;
                appendMessage(answer, "bot-msg");
            })
            .catch(() => {
                typing.style.display = "none";
                appendMessage("Erro de comunicação com o servidor.", "bot-msg error");
            });
    });

    function appendMessage(text, className) {
        const msg = document.createElement("div");
        msg.className = className;
        msg.textContent = text;
        messages.appendChild(msg);
    }
});
