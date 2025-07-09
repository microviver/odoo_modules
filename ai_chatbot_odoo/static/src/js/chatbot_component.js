/** @odoo-module **/

import { Component, mount } from "@odoo/owl";

class ChatbotComponent extends Component {
    static template = "ai_chatbot_odoo.ChatbotTemplate";

    state = {
        visible: false,
        message: "",
        messages: [],
    };

    toggleChatbot() {
        this.state.visible = !this.state.visible;
    }

    onInput(ev) {
        this.state.message = ev.target.value;
    }

    sendMessage(ev) {
        ev.preventDefault();
        if (this.state.message.trim()) {
            this.state.messages.push({ text: this.state.message, from: "user" });
            this.state.message = "";
        }
    }
}

mount(ChatbotComponent, { target: document.body });

