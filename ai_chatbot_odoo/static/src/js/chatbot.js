/** @odoo-module */

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

        // Esconde inicialmente o box
        const box = document.getElementById("chatbot-box");
        if (box) {
            box.style.display = "none";
        }

        // Ativa manualmente ao clicar no botão
        const btn = document.querySelector(".activate-chatbot");
        if (btn) {
            btn.addEventListener("click", () => {
                box.style.display = "block";
                this.inputField.focus();
            });
        }

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

        this._appendMessage("user", question);
        this.inputField.value = "";
        this.typingIndicator.style.display = "block";

        fetch("/ai_chatbot/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ question }),
        })
            .then((res) => res.json())
            .then((data) => {
                this.typingIndicator.style.display = "none";
                if (data.answer) {
                    this._appendMessage("bot", data.answer);
                } else {
                    this._appendMessage("bot", "Erro: " + data.error);
                }
            })
            .catch((err) => {
                this.typingIndicator.style.display = "none";
                this._appendMessage("bot", "Falha de conexão.");
            });
    },

    _appendMessage(from, text) {
        const message = document.createElement("div");
        message.className = `chatbot-message ${from}`;
        message.textContent = text;
        this.messageContainer.appendChild(message);
        this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
    },
});

