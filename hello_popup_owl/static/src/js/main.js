/** @odoo-module **/
import { mount } from "@odoo/owl";
import { PopupComponent } from "../components/popup/popup_component";

document.addEventListener("DOMContentLoaded", async () => {
    const container = document.createElement("div");
    document.body.appendChild(container);
    await mount(PopupComponent, { target: container });
});