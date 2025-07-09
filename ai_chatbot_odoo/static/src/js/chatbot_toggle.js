/** @odoo-module **/

import publicWidget from 'web.public.widget';

publicWidget.registry.ChatbotToggle = publicWidget.Widget.extend({
    selector: '.activate-chatbot',

    events: {
        click: '_onToggleChatbot',
    },

    start() {
        const header = document.querySelector('#chatbot-header');
        if (header) {
            header.addEventListener('click', this._onToggleChatbot.bind(this));
        }
        return this._super(...arguments);
    },

    _onToggleChatbot() {
        const box = document.querySelector('#chatbot-box');
        if (box) {
            const visible = box.style.display === 'block';
            box.style.display = visible ? 'none' : 'block';
        }
    }
});

