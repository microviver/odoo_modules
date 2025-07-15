// File: static/src/js/main.js
import { mount } from "@odoo/owl";
import { ChatbotComponent } from "../components/chatbot/chatbot_component";

document.addEventListener("DOMContentLoaded", () => {
    const target = document.createElement("div");
    document.body.appendChild(target);
    mount(ChatbotComponent, { target });
});
