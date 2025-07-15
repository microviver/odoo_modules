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
        this.state = useState({ visible: false });

        this.toggle = () => {
            this.state.visible = !this.state.visible;
        };
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const target = document.createElement("div");

    // Isso evita que o website builder tente editar a UI do botão
    target.dataset.oeContext = "non-editable";
    target.setAttribute("data-no-drag", "true");
    target.setAttribute("data-no-highlight", "true");

    target.style.position = "relative";
    document.body.appendChild(target);
    mount(ChatbotWrapper, { target });
});
