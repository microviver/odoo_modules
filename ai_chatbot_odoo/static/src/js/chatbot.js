/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.chatbotWidget = publicWidget.Widget.extend({
    selector: '.activate-chatbot',
    events: {
        'click': '_onClickActivateChatbot'
    },

    _onClickActivateChatbot() {
        if (!document.getElementById("chatbot-box")) {
            this._createChatbotBox();
        }
    },

    _createChatbotBox() {
        const chatbotBox = document.createElement("div");
        chatbotBox.id = "chatbot-box";
        chatbotBox.innerHTML = `
            <div id="chatbot-header">Simbi 🤖</div>
            <div id="chatbot-messages"></div>
            <div id="chatbot-typing"><em>piensando...</em></div>
            <input type="text" id="chatbot-input" placeholder="Escreve algo..." />
        `;
        document.body.appendChild(chatbotBox);

        this._setupChatbotEvents();
    },

    _setupChatbotEvents() {
        const typingIndicator = document.getElementById("chatbot-typing");
        const inputField = document.getElementById("chatbot-input");
        const messageContainer = document.getElementById("chatbot-messages");

        typingIndicator.style.display = "none";

        inputField.addEventListener("keypress", function (e) {
            if (e.key === "Enter") {
                const question = inputField.value.trim();
                if (!question) return;

                const userMsg = document.createElement("div");
                userMsg.className = "user-msg";
                userMsg.textContent = question;
                messageContainer.appendChild(userMsg);

                inputField.value = "";
                typingIndicator.style.display = "block";

                fetch("/ai_chatbot/ask", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ question }),
                })
                .then((res) => res.json())
                .then((data) => {
                    typingIndicator.style.display = "none";
                    const botMsg = document.createElement("div");
                    botMsg.className = "bot-msg";
                    botMsg.textContent = data.answer || `Erro: ${data.error}`;
                    messageContainer.appendChild(botMsg);
                })
                .catch(() => {
                    typingIndicator.style.display = "none";
                    const errorMsg = document.createElement("div");
                    errorMsg.className = "bot-msg error";
                    errorMsg.textContent = "Erro de comunicação com o servidor.";
                    messageContainer.appendChild(errorMsg);
                });
            }
        });
    }
});

