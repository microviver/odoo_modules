/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.chatbotController = publicWidget.Widget.extend({
    selector: 'body',

    events: {
        'click .activate-chatbot': '_onActivateClick',
        'click #chatbot-header': '_onHeaderClick',
        'keypress #chatbot-input': '_onKeyPress',
    },

    start() {
        this.chatbox = document.getElementById('chatbot-box');
        this.typingIndicator = document.getElementById('chatbot-typing');
        this.inputField = document.getElementById('chatbot-input');
        this.messageContainer = document.getElementById('chatbot-messages');

        if (this.chatbox) {
            this.chatbox.style.display = 'none'; // Oculta no início
        }

        if (this.typingIndicator) {
            this.typingIndicator.style.display = "none";
        }

        return this._super(...arguments);
    },

    _onActivateClick() {
        if (this.chatbox) {
            this.chatbox.style.display = 'block';
        }
    },

    _onHeaderClick() {
        if (this.chatbox) {
            this.chatbox.style.display = 'none';
        }
    },

    _onKeyPress(ev) {
        if (ev.key === "Enter") {
            this._handleInput();
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

