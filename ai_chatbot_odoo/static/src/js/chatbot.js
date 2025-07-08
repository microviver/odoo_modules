/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

const ChatbotWidget = publicWidget.Widget.extend({
    template: null,  // não usamos um template Odoo, renderizamos HTML no start
    selector: null,  // não usamos auto-bind via seletor

    start() {
        this._renderChatbotBox();
        this._setupChatbot();
        return this._super(...arguments);
    },

    _renderChatbotBox() {
        this.el = document.createElement("div");
        this.el.id = "chatbot-box";
        this.el.innerHTML = `
            <div id="chatbot-header">Simbi 🤖</div>
            <div id="chatbot-messages"></div>
            <div id="chatbot-typing"><em>piensando...</em></div>
            <input type="text" id="chatbot-input" placeholder="Escreve algo..." />
        `;
        document.body.appendChild(this.el);
    },

    _setupChatbot() {
        this.typingIndicator = this.el.querySelector("#chatbot-typing");
        this.inputField = this.el.querySelector("#chatbot-input");
        this.messageContainer = this.el.querySelector("#chatbot-messages");

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
            .then((res) => res.json())
            .then((data) => {
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

// Ativação manual quando DOM estiver carregado
document.addEventListener("DOMContentLoaded", () => {
    const chatbot = new ChatbotWidget();
    chatbot.appendTo(document.body);
});
