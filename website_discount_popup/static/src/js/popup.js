/** @odoo-module **/

document.addEventListener("DOMContentLoaded", () => {
    const popup = document.getElementById("discountPopup");
    const btn = document.getElementById("submitDiscountBtn");
    const emailInput = document.getElementById("discountEmail");

    if (popup && !localStorage.getItem("discountPopupShown")) {
        setTimeout(() => {
            popup.style.display = "block";
            localStorage.setItem("discountPopupShown", "true");
        }, 1000);
    }

    const isValidEmail = (email) =>
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());

    btn?.addEventListener("click", () => {
        const email = emailInput?.value.trim();

        if (!isValidEmail(email)) {
            alert("Digite um e-mail válido!");
            return;
        }

        fetch("/discount/email", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest",
            },
            body: JSON.stringify({ email }),
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.success) {
                    alert("Desconto aplicado! Verifique seu e-mail.");
                    popup.style.display = "none";
                } else {
                    alert("Erro: " + (data.error || "Algo deu errado."));
                }
            })
            .catch(() => {
                alert("Erro de comunicação com o servidor.");
            });
    });
});
