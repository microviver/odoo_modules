/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class SimpleCounter extends Component {
    static template = 'custom_js_owl.SimpleCounter';
    setup() {
        this.state = useState({ value: 0 });
    }
    increment() {
        this.state.value++;
    }
}
