/** static/src/js/main.js **/
import { mount, Component, useState } from "@odoo/owl";
import { ChatbotComponent } from "../components/chatbot/chatbot_component";

class ChatbotWrapper extends Component {
    static template = `
    <div>
      <button class="chatbot-toggle-button" t-on-click="toggle">🤖</button>
      <t t-if="state.visible">
        <ChatbotComponent/>
      </t>
    </div>`;

    setup() {
        console.log("✅ ChatbotWrapper.setup");
        this.state = useState({ visible: false });

        this.toggle = () => {
            console.log("🔁 Toggle chamado");
            this.state.visible = !this.state.visible;
        };
    }
}

document.addEventListener("DOMContentLoaded", () => {
    console.log("✅ DOMContentLoaded disparado");

    const target = document.createElement("div");
    target.style.position = "relative";
    target.id = "chatbot-wrapper-root";

    document.body.appendChild(target);

    console.log("📌 Mounting chatbot...");
    mount(ChatbotWrapper, { target });
});
