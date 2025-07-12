/** @odoo-module **/

import { Dialog } from "@web/core/dialog/dialog";
import { registry } from "@web/core/registry";
import { PopupComponent } from "../components/popup/popup_component"; // Import your component

// This component will be responsible for triggering the dialog
// It could be a simple action in the frontend, or integrated into an existing component
export const showPopup = () => {
    const dialogService = registry.category("services").get("dialog");
    dialogService.add(PopupComponent, {
        title: "Offer!", // Title for the dialog
        onClose: () => {
            console.log("Popup closed");
            // You can add logic here for when the popup is closed
        },
        // Any props you want to pass to your PopupComponent
    });
};

// You might want to expose this function globally or through a specific Odoo mechanism
// For demonstration, let's just make it show on page load for now.
// In a real scenario, you'd trigger `showPopup()` based on an event (e.g., button click, timer).

// Example: To show it immediately on page load, similar to your original intent:
// You would typically add a website controller that calls this, or hook into an existing frontend component.
// For a quick test, you could add this in a template or another JS file that gets loaded.
// This is a simplified direct call for immediate testing.
// A more Odoo-idiomatic way would be to have a website controller render a template that includes
// a small script to call this function.
// Or, you can extend an existing Odoo component and call it from there.

// For immediate display on page load (for testing):
// You would likely have a separate file or embed this directly in a QWeb template
// that is loaded on the website homepage.
// Example of a simple way to call it from a template's JS:
// Assume you have a QWeb template that loads this `popup_service.js`
// And then in a <script> tag within that template, you could do:
// import { showPopup } from 'hello_popup_owl/static/src/js/popup_service';
// showPopup();

// For a more integrated approach, you would add a QWeb template
// which includes a small script that calls 'showPopup'
// This `showPopup` function could be exposed via the registry or called from a custom widget.