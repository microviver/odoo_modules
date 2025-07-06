console.log("popup.js carregado")
odoo.define('website_discount_popup.popup', function (require) {
    'use strict';

    const publicWidget = require('web.public.widget');

    publicWidget.registry.DiscountPopup = publicWidget.Widget.extend({
        selector: 'body',
        start: function () {
            const popup = document.getElementById('discountPopup');
            const btn = document.getElementById('submitDiscountBtn');

            if (popup && !localStorage.getItem('discountPopupShown')) {
                setTimeout(() => {
                    popup.style.display = 'block';
                    localStorage.setItem('discountPopupShown', 'true');
                }, 1000);
            }

            if (btn) {
                btn.addEventListener('click', function () {
                    const email = document.getElementById("discountEmail").value;
                    if (!email) return alert("Digite um email válido!");
                    fetch("/discount/email", {
                        method: "POST",
                        headers: { 
                            "Content-Type": "application/json",
                            "X-CSRFToken": odoo.csrf_token
                        },
                        body: JSON.stringify({ email: email }),
                    }).then(() => {
                        popup.innerHTML = "<p>Obrigado! Desconto aplicado.</p>";
                    });
                });
            }

            return this._super(...arguments);
        },
    });

    return publicWidget.registry.DiscountPopup;
});
