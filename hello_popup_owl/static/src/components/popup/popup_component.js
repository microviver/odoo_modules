/** @odoo-module **/
import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { registry } from "@web/core/registry";

export class PopupComponent extends Component {
    static template = "hello_popup_owl.PopupComponent";
    static components = { Dialog };

    setup() {
        this.state = useState({
            visible: true,
            email: "",
        });
    }

    close() {
        this.state.visible = false;
    }
}

registry.category("public_components").add("hello_popup_owl.PopupComponent", PopupComponent);
