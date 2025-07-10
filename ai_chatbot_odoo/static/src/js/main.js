/** @odoo-module **/

import { mount } from "@odoo/owl";
import { Chatbot } from "../components/Chatbot/chatbot_component";

document.addEventListener("DOMContentLoaded", () => {
    const container = document.createElement("div");
    document.body.appendChild(container);
    mount(Chatbot, { target: container });
});

