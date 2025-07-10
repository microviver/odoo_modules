/** @odoo-module **/

import { ChatbotComponent } from "@ai_chatbot_odoo/components/chatbot/chatbot_component";
import { mount } from "@odoo/owl";

document.addEventListener("DOMContentLoaded", () => {
    const target = document.querySelector("#chatbot-placeholder") || document.body;

    mount(ChatbotComponent, {
        target,
        position: "last",  // Ou "first" / "before" / "after"
    });
});

