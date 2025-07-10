/** @odoo-module **/

import { mount } from "@odoo/owl";
import { Chatbot } from "@ai_chatbot_odoo/components/chatbot/chatbot_component";

document.addEventListener("DOMContentLoaded", () => {
    const el = document.getElementById("chatbot-mount");
    if (el) {
        mount(Chatbot, { target: el });
    } else {
        console.warn("chatbot-mount não encontrado.");
    }
});

