/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

class Popup extends Component {
    setup() {
        this.state = useState({ visible: true });
    }

    hidePopup() {
        this.state.visible = false;
    }
}

Popup.template = "hello_popup.Popup";
registry.category("public_components").add("hello_popup.Popup", Popup);
export { Popup };
