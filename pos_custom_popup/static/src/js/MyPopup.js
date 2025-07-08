import { Popup } from "@point_of_sale/app/components/Popups/Popup";
import { useState } from "@odoo/owl";

export class MyPopup extends Popup {
    setup() {
        super.setup();
        this.state = useState({ userInput: "" });
    }

    getPayload() {
        return this.state.userInput;
    }
}

MyPopup.template = "MyPopup";