/** @odoo-module **/
import { mount } from "@odoo/owl";
import { HomepageAlert } from "../components/homepage_alert";

document.addEventListener("DOMContentLoaded", () => {
    const target = document.getElementById("homepage-alert-root");
    if (target) {
        mount(HomepageAlert, { target });
    }
});

