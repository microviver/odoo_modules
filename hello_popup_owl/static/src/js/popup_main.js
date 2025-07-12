/** @odoo-module **/

import { registry } from "@web/core/registry";
import { startService } from "@odoo/owl";
import { services } from "@web/core/utils/services";
import { PopupComponent } from "../components/popup/popup_component"; // Correct relative import

async function showMyPopup() {
    // These lines are crucial for setting up the OWL environment
    const owl_services = await startService(services);
    const env = owl_services; // makeEnv is automatically done when using startService
                            // and accessing services directly from the env.
                            // MakeEnv is more for isolated tests.

    const dialogService = registry.category("services").get("dialog");
    const helloPopupComponent = registry.category("public_components").get("hello_popup_owl.PopupComponent");

    if (dialogService && helloPopupComponent) {
        console.log("Attempting to add dialog from popup_main.js.");
        dialogService.add(helloPopupComponent, {
            title: "Oferta Especial!", // Title for the dialog
            onClose: () => {
                console.log("Popup fechado.");
                sessionStorage.setItem('helloPopupShown', 'true');
            },
        });
    } else {
        console.error("Dialog service or PopupComponent not found in popup_main.js.");
    }
}

// Trigger the popup when the page loads
// Using `window.addEventListener('load', ...)` or equivalent
// ensures the DOM and all other assets are loaded.
// Odoo's asset system also has mechanisms to ensure scripts run at the right time.
// For a simple module, this could be a direct call, or hooked into a website event.

// For immediate testing after page load:
// You can register a public widget or just run it.
// A common way for site-wide scripts is to run after the web client is ready.
// For Website frontend, a simple DOMContentLoaded check is usually fine.

document.addEventListener('DOMContentLoaded', () => {
    if (!sessionStorage.getItem('helloPopupShown')) {
        console.log("DOM loaded. Session storage item not found, calling showMyPopup from popup_main.js.");
        showMyPopup();
    } else {
        console.log("DOM loaded. Popup already shown (session storage) from popup_main.js.");
    }
});