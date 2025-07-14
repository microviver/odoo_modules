/** @odoo-module **/

import { registry } from "@web/core/registry";

document.addEventListener('DOMContentLoaded', () => {
    const button = document.getElementById('open-popup-button');

    if (button) {
        button.addEventListener('click', () => {
            const dialogService = registry.category("services").get("dialog");
            const PopupComponent = registry.category("public_components").get("hello_popup_owl.PopupComponent");

            if (dialogService && PopupComponent) {
                dialogService.add(PopupComponent, {
                    title: "Oferta Especial!",
                    onClose: () => {
                        console.log("Popup fechado.");
                    },
                });
            } else {
                console.error("Dialog service ou PopupComponent não encontrado.");
            }
        });
    }
});
