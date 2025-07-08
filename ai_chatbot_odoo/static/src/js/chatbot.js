/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.chatbotWidget = publicWidget.Widget.extend({
    selector: '#chatbot-box',

    start() {
        this._setupChatbot();
        return this._super(...arguments);
    },

    _setupChatbot() {
        this.typingIndicator = document.getElementById("chatbot-typing");
        this.inputField = document.getElementById("chatbot-input");
        this.messageContainer = document.getElementById("chatbot-messages");

        if (this.typingIndicator) {
            this.typingIndicator.style.display = "none";
        }

        if (this.inputField) {
            this.inputField.addEventListener("keypress", (e) => {
                if (e.key === "Enter") {
                    this._handleInput();
                }
            });
        }
    },

    _handleInput() {
        const question = this.inputField.value.trim();
        if (!question) return;

        const userMsg = document.createElement("div");
        userMsg.className = "user-msg";
        userMsg.textContent = question;
        this.messageContainer.appendChild(userMsg);

        this.inputField.value = "";
        this.typingIndicator.style.display = "block";

        fetch("/ai_chatbot/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ question }),
        })
        .then(res => res.json())
        .then(data => {
            this.typingIndicator.style.display = "none";
            const botMsg = document.createElement("div");
            botMsg.className = "bot-msg";
            botMsg.textContent = data.answer || `Erro: ${data.error}`;
            this.messageContainer.appendChild(botMsg);
        })
        .catch(() => {
            this.typingIndicator.style.display = "none";
            const errorMsg = document.createElement("div");
            errorMsg.className = "bot-msg error";
            errorMsg.textContent = "Erro de comunicação com o servidor.";
            this.messageContainer.appendChild(errorMsg);
        });
    },
});

