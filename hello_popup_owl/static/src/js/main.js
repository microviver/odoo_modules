/** @odoo-module **/
import { mount } from "@odoo/owl";
import { Component } from "@odoo/owl";

document.addEventListener("DOMContentLoaded", () => {
  const el = document.getElementById("popup-mount");
  if (el) {
    const publicComponent = registry
      .category("public_components")
      .get("hello_popup_owl.PopupComponent");
    mount(publicComponent, { target: el });
  }
});
