/** @odoo-module **/

import { mount } from "@odoo/owl";
import { Chatbot } from "@ai_chatbot_odoo/components/chatbot/chatbot_component";

document.addEventListener("DOMContentLoaded", async () => {
    const div = document.createElement("div");
    div.id = "chatbot-mount";
    document.body.appendChild(div);  // ou `wrap`, se quiser dentro do conteúdo

    await mount(Chatbot, {
        target: div,
    });
});
