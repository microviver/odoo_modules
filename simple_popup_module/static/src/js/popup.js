/** @odoo-module **/

import { Component } from "@odoo/owl";

export class SimplePopup extends Component {
    static template = "popup_demo.SimplePopup";

    setup() {
        console.log("Popup carregado!");
    }
}

