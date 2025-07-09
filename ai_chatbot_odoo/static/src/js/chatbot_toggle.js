/** @odoo-module **/

import { Component, onMounted, useRef } from "@odoo/owl";
import { mount } from "@odoo/owl";

class ChatbotToggle extends Component {
    setup() {
        this.chatbotBox = useRef("chatbotBox");
        this.button = useRef("toggleButton");

        onMounted(() => {
            this.button.el.addEventListener("click", this.toggleChat.bind(this));
        });
    }

    toggleChat() {
        const box = this.chatbotBox.el;
        if (box.style.display === "none" || !box.style.display) {
            box.style.display = "block";
        } else {
            box.style.display = "none";
        }
    }
}

ChatbotToggle.template = "ai_chatbot_odoo.ChatbotToggle";

export default ChatbotToggle;

// Mount it manually
document.addEventListener("DOMContentLoaded", () => {
    const target = document.getElementById("chatbotContainer");
    if (target) {
        mount(ChatbotToggle, { target });
    }
});

