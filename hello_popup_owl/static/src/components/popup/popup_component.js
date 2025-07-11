/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class PopupComponent extends Component {
  static template = "hello_popup_owl.PopupComponent";

  setup() {
    this.state = useState({ show: true });
  }

  close() {
    this.state.show = false;
  }
}

registry.category("public_components").add("hello_popup_owl.PopupComponent", {
  Component: PopupComponent,
});
