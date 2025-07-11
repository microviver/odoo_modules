/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class PopupComponent extends Component {
    static template = "hello_popup_owl.PopupComponent";
    static components = { Dialog };

    setup() {
        this.state = useState({ visible: true });
    }

    close() {
        this.state.visible = false;
    }
}
