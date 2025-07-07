/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.DiscountPopup = publicWidget.Widget.extend({
    selector: 'body',

    start: function () {
        const popup = document.getElementById('discountPopup');
        const btn = document.getElementById('submitDiscountBtn');

        // Mostra o popup se ainda não foi exibido
        if (popup && !localStorage.getItem('discountPopupShown')) {
            setTimeout(() => {
                popup.style.display = 'block';
                localStorage.setItem('discountPopupShown', 'true');
            }, 1000);
        }

        // Submete o e-mail
        if (btn) {
            btn.addEventListener('click', function () {
                const email = document.getElementById("discountEmail").value;
                if (!email || !email.includes('@')) {
                    return alert("Digite um e-mail válido!");
                }

                fetch("/discount/email", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "
