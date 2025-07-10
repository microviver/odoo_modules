/** @odoo-module **/

import { mount } from "@odoo/owl";
import { Chatbot } from "@ai_chatbot_odoo/components/chatbot/chatbot_component";

document.addEventListener("DOMContentLoaded", async () => {
    const mountEl = document.getElementById("chatbot-mount");
    if (mountEl) {
        console.log("Montando chatbot OWL...");
        await mount(Chatbot, { target: mountEl });
    } else {
        console.warn("Elemento #chatbot-mount não encontrado.");
    }
});

