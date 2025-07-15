/** static/src/components/chatbot/chatbot_component.js **/
import { Component, useState, onMounted } from "@odoo/owl";

export class ChatbotComponent extends Component {
    static template = "ai_chatbot_odoo.ChatbotTemplate";

    setup() {
        this.messages = useState([]);
        this.userInput = useState("");
    }

    async sendMessage(ev) {
        ev.preventDefault();
        if (this.userInput.trim()) {
            this.messages.push({ from: "user", text: this.userInput });
            const userMessage = this.userInput;
            this.userInput = "";

            // Simula resposta (ou conecta à tua API)
            this.messages.push({ from: "bot", text: "🤖 Estou a pensar..." });

            setTimeout(() => {
                this.messages.push({ from: "bot", text: "Resposta automática para: " + userMessage });
            }, 1000);
        }
    }
}
