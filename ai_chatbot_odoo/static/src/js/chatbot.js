odoo.define('ai_chatbot_odoo.chatbot', function (require) {
    'use strict';

    const publicWidget = require('web.public.widget');

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
            const message = this.inputField.value.trim();
            if (!message) return;

            this._appendMessage("user-msg", message);
            this.inputField.value = '';
            this.typingIndicator.style.display = "block";

            this._askChatbot(message);
        },

        _appendMessage(type, text) {
            const div = document.createElement("div");
            div.className = type;
            div.innerText = text;
            this.messageContainer.appendChild(div);
            this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
        },

        _askChatbot(message) {
            fetch('/ai_chatbot/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: message }),
            })
            .then(response => response.json())
            .then(data => {
                this.typingIndicator.style.display = "none";
                if (data.answer) {
                    this._appendMessage("bot-msg", data.answer);
                } else if (data.error) {
                    this._appendMessage("bot-msg error", "Erro: " + data.error);
                }
            })
            .catch(err => {
                this.typingIndicator.style.display = "none";
                this._appendMessage("bot-msg error", "Erro na requisição.");
            });
        }
    });

    // Ativação manual via botão
    document.addEventListener('DOMContentLoaded', () => {
        const activateBtn = document.getElementById("activate-chatbot-btn");
        const chatbotBox = document.getElementById("chatbot-box");

        if (activateBtn && chatbotBox) {
            activateBtn.addEventListener("click", () => {
                chatbotBox.style.display = chatbotBox.style.display === "none" ? "block" : "none";
                if (chatbotBox.style.display === "block") {
                    publicWidget.registry.chatbotWidget.prototype.start.call({
                        el: chatbotBox,
                        $el: $(chatbotBox),
                        _super: function () {},
                    });
                }
            });
        }
    });
});

