/** @odoo-module **/

import { mount } from "@odoo/owl";
import { PopupComponent } from "../components/popup/popup_component";

document.addEventListener("DOMContentLoaded", function () {
    const mountPoint = document.querySelector("#popup-mount");
    if (mountPoint) {
        mount(PopupComponent, { target: mountPoint });
    }
});
