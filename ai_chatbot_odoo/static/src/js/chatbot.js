/** @odoo-module */

import { loadJS } from "@web/core/assets";
import { jsonrpc } from "@web/core/network/rpc";

document.addEventListener("DOMContentLoaded", () => {
    const box = document.getElementById("chatbot-box");
    const input = document.getElementById("chatbot-input");
    const messages = document.getElementById("chatbot-messages");
    const typing = document.getElementById("chatbot-typing");

    if (!box || !input) return;

    input.addEventListener("keypress", async (event) => {
        if (event.key === "Enter" && input.value.trim() !== "") {
            const question = input.value.trim();
            input.value = "";
            typing.style.display = "block";
            messages.innerHTML += `<div class="user-message">${question}</div>`;

            try {
                const response = await jsonrpc("/ai_chatbot/ask", { question });
                messages.innerHTML += `<div class="bot-message">${response.answer || "..."}</div>`;
            } catch (error) {
                messages.innerHTML += `<div class="bot-message error">Erro: ${error.message}</div>`;
            }

            typing.style.display = "none";
        }
    });
});

