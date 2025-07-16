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
    const isWebsiteEditor = !!document.body.classList.contains("editor_enable");
    if (isWebsiteEditor) {
        console.warn("🛑 Website Builder ativo - chatbot não será montado.");
        return;
    }

    console.log("✅ DOM pronto - montando ChatbotWrapper...");

    const target = document.createElement("div");
    target.id = "chatbot-wrapper-root";
    target.style.position = "relative";  
    document.body.appendChild(target);

    mount(ChatbotWrapper, { target });
});

const style = document.createElement("style");
style.textContent = `
    .chatbot-toggle-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 99999;
        background-color: red;
        color: white;
        border: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 30px;
    }
`;
document.head.appendChild(style);
