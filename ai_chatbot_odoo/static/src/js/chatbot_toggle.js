/** @odoo-module **/

import { publicWidget } from "@web/env";

publicWidget.registry.ChatbotToggle = publicWidget.Widget.extend({
    selector: '.activate-chatbot',
    events: {
        click: '_onToggleChatbot',
        'click #chatbot-header': '_onToggleChatbot',
    },

    _onToggleChatbot() {
        const chatbotBox = document.querySelector('#chatbot-box');
        if (chatbotBox) {
            const isVisible = chatbotBox.style.display === 'block';
            chatbotBox.style.display = isVisible ? 'none' : 'block';
        }
    }
});

