/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.discountPopup = publicWidget.Widget.extend({
  selector: '#discountPopup',
  start() {
    if (!localStorage.getItem('discountPopupShown')) {
      setTimeout(() => {
        this.el.style.display = 'block';
        localStorage.setItem('discountPopupShown', 'true');
      }, 1000);
    }
  },
  events: {
    'click #submitDiscountBtn': '_onClickSubmit',
  },
  _onClickSubmit(ev) {
    ev.preventDefault();
    const email = this.el.querySelector('#discountEmail').value.trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return alert("Digite um e‑mail válido!");
    }
    fetch("/discount/email", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest" },
      body: JSON.stringify({ email }),
    }).then(r => r.json()).then(data => {
      alert(data.success ? "Desconto aplicado!" : `Erro: ${data.error || 'Algo deu errado.'}`);
      if (data.success) this.el.style.display = 'none';
    }).catch(() => alert("Erro de comunicação com o servidor."));
  },
});

