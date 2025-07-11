/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

class Popup extends Component {
    closePopup() {
        this.el.remove();
    }
}

Popup.template = "hello_popup_owl.Popup";
registry.category("public_components").add("hello_popup_owl.Popup", Popup);

export { Popup };
