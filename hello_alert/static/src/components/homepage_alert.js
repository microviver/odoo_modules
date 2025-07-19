/** @odoo-module **/

import { Component, useState } from 'owl';

export class HomepageAlert extends Component {
    state = useState({ email: '', shown: false });

    mounted() {
        if (localStorage.getItem('popupShown')) {
            this.state.shown = false;
        } else {
            this.state.shown = true;
        }
    }

    onSubmit() {
        if (this.state.email.includes('@')) {
            alert('Obrigado! Desconto garantido!');
            localStorage.setItem('popupShown', 'true');
            this.state.shown = false;
        } else {
            alert('Email inválido!');
        }
    }
}

HomepageAlert.template = 'user.HomepageAlert';
