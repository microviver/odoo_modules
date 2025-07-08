import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class PopupButton extends Component {
    setup() {
        this.pos = usePos();
    }

    async onClick() {
        const { confirmed, payload } = await this.pos.gui.showPopup("MyPopup", {
            title: "Hello World",
            body: "This is a custom popup.",
        });

        if (confirmed) {
            this.pos.env.services.notify.show(`You entered: ${payload}`);
        }
    }
}

PopupButton.template = "PopupButton";