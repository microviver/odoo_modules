/** @odoo-module **/

import { mount } from "@odoo/owl";
import { PopupComponent } from "../components/popup/popup_component";


window.addEventListener("DOMContentLoaded", () => {
    const target = document.getElementById("popup-mount");
    if (target) {
        mount(PopupComponent, target, {});
    }
});

