/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.chatbotWidget = publicWidget.Widget.extend({
    selector: '.activate-chatbot', // Botão que ativa o chatbot
    events: {
        'click': '_onActivateClick',
    },

    start() {
        this.chatbox = document.getElementById('chatbot-box');
        this.typingIndicator = document.getElementById('chatbot-typing');
        this.inputField = document.getElementById('chatbot-input');
        this.messageContainer = document.getElementById('chatbot-messages');
        this.chatHeader = document.getElementById('chatbot-header');

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

        if (this.chatHeader && this.chatbox) {
            this.chatHeader.style.cursor = "pointer";
            this.chatHeader.addEventListener("click", () => {
                this.chatbox.style.display = "none";
            });
        }

        return this._super(...arguments);
    },

    _onActivateClick() {
        if (this.chatbox) {
            this.chatbox.style.display = "block";
        }
    },

    async _handleInput() {
        const question = this.inputField.value.trim();
        if (!question) return;

        this._appendMessage("user", question);
        this.inputField.value = "";
        this.typingIndicator.style.display = "block";

        try {
            const response = await fetch("/ai_chatbot/ask", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ question }),
            });

            const data = await response.json();
            this.typingIndicator.style.display = "none";
            if (data.answer) {
                this._appendMessage("bot", data.answer);
            } else {
                this._appendMessage("bot", "Erro: " + (data.error || "sem resposta"));
            }
        } catch (err) {
            this.typingIndicator.style.display = "none";
            this._appendMessage("bot", "Erro técnico ao chamar o assistente.");
        }
    },

    _appendMessage(sender, text) {
        const messageElem = document.createElement("div");
        messageElem.className = sender === "user" ? "chatbot-user" : "chatbot-bot";
        messageElem.textContent = text;
        this.messageContainer.appendChild(messageElem);
        this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
    }
});

