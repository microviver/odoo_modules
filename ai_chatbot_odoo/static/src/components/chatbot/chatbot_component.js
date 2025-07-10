/** @odoo-module **/

import { Component, useState, onMounted } from "@odoo/owl";

export class Chatbot extends Component {
    setup() {
        this.state = useState({
            messages: [],
            typing: false,
            input: "",
        });

        onMounted(() => {
            this.scrollToBottom();
        });
    }

    async sendMessage() {
        const question = this.state.input.trim();
        if (!question) return;

        this.state.messages.push({ sender: "user", text: question });
        this.state.input = "";
        this.state.typing = true;

        try {
            const response = await fetch("/ai_chatbot/ask", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ question }),
            });

            const data = await response.json();
            this.state.typing = false;

            this.state.messages.push({
                sender: "bot",
                text: data.answer || "Erro: " + (data.error || "sem resposta"),
            });
        } catch (e) {
            this.state.typing = false;
            this.state.messages.push({
                sender: "bot",
                text: "Erro técnico ao chamar o assistente.",
            });
        }

        this.scrollToBottom();
    }

    scrollToBottom() {
        setTimeout(() => {
            const el = this.el.querySelector("#chatbot-messages");
            if (el) el.scrollTop = el.scrollHeight;
        }, 100);
    }

    toggleBox() {
        this.el.querySelector("#chatbot-box").classList.toggle("hidden");
    }

    onKeyPress(ev) {
        if (ev.key === "Enter") {
            this.sendMessage();
        }
    }
}

Chatbot.template = "ai_chatbot_odoo.components.chatbot.chatbot_template";

