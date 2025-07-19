/** @odoo-module **/
import { Component, useState } from "@odoo/owl";

export class HomepageAlert extends Component {
    static template = "my_homepage_module.HomepageAlert";

    setup() {
        this.state = useState({ show: true });
    }

    closeAlert() {
        this.state.show = false;
    }
}

