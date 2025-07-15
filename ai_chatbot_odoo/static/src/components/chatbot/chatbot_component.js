// File: static/src/components/chatbot/chatbot_component.js
import { Component, useState, onMounted } from "@odoo/owl";

export class ChatbotComponent extends Component {
    static template = "ai_chatbot_odoo.ChatbotTemplate";

    setup() {
        this.messages = useState([]);
        this.inputValue = useState("");
        this.loading = useState(false);

        this.sendMessage = async () => {
            const question = this.inputValue.trim();
            if (!question) return;
            this.messages.push({ text: question, type: "user" });
            this.inputValue = "";
            this.loading = true;

            try {
                const res = await fetch("/ai_chatbot/ask", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ question }),
                });
                const data = await res.json();
                this.messages.push({
                    text: data.answer || data.error || "Erro",
                    type: "bot",
                });
            } catch (e) {
                this.messages.push({ text: "Erro de rede", type: "bot" });
            }
            this.loading = false;
        };
    }
}
