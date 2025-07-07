/** @odoo-module **/

document.addEventListener("DOMContentLoaded", function () {
    const popup = document.getElementById('discountPopup');
    const btn = document.getElementById('submitDiscountBtn');

    // Mostrar o popup se ainda não foi exibido
    if (popup && !localStorage.getItem('discountPopupShown')) {
        setTimeout(() => {
            popup.style.display = 'block';
            localStorage.setItem('discountPopupShown', 'true');
        }, 1000);
    }

    // Submeter o e-mail
    if (btn) {
        btn.addEventListener('click', function () {
            const email = document.getElementById("discountEmail").value;
            if (!email || !email.includes('@')) {
                alert("Digite um e-mail válido!");
                return;
            }

            fetch("/discount/email", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
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
