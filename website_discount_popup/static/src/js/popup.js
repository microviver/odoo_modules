/** @odoo-module **/

document.addEventListener("DOMContentLoaded", function () {
    const popup = document.getElementById('discountPopup');
    const btn = document.getElementById('submitDiscountBtn');
    const emailInput = document.getElementById('discountEmail');

    if (popup && !localStorage.getItem('discountPopupShown')) {
        setTimeout(() => {
            popup.style.display = 'block';
            localStorage.setItem('discountPopupShown', 'true');
        }, 1000);
    }

    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    if (btn && emailInput && popup) {
        btn.addEventListener('click', function () {
            const email = emailInput.value.trim();
            if (!isValidEmail(email)) {
                alert("Digite um e-mail válido!");
                return;
            }

            fetch("/discount/email", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest"
                },
                body: JSON.stringify({ email }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Desconto aplicado! Verifique seu e-mail.");
                    popup.style.display = 'none';
                } else {
                    alert("Erro: " + (data.error || "Algo deu errado."));
                }
            })
            .catch(() => {
                alert("Erro de comunicação com o servidor.");
            });
        });
    }
});
