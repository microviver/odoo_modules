/** @odoo-module **/

import { mount } from "@odoo/owl";
import { Popup } from "@hello_popup_owl/components/popup/popup_component";

document.addEventListener("DOMContentLoaded", () => {
    const mountEl = document.getElementById("popup-mount");
    if (mountEl) {
        mount(Popup, { target: mountEl });
    }
});
