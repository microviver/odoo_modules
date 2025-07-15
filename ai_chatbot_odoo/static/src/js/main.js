/** static/src/js/main.js **/
import { mount, Component, useState } from "@odoo/owl";
import { ChatbotComponent } from "../components/chatbot/chatbot_component";

class ChatbotWrapper extends Component {
    static template = `
    <div>
      <button class="chatbot-toggle-button" t-on-click="toggle">🤖</button>
      <ChatbotComponent t-if="visible" visible="visible"/>
    </div>`;

    setup() {
        this.visible = useState(false);
        this.toggle = () => {
            this.visible = !this.visible;
        };
    }

    get visible() {
        return this.state;
    }

    get ChatbotComponent() {
        return ChatbotComponent;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const target = document.createElement("div");
    document.body.appendChild(target);
    mount(ChatbotWrapper, { target });
});
