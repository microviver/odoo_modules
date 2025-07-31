from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class PartnerDniCheckout(WebsiteSale):

    # Este método é chamado para guardar os dados do formulário no parceiro
    # Vamos usá-lo para garantir que o campo 'name' é preenchido corretamente
    def _checkout_form_save(self, mode, checkout, all_form_fields):
        # 1. Preenche o campo 'name' no dicionário 'checkout' antes de chamar a lógica do Odoo.
        first_name = checkout.get('first_name', '').strip()
        last_name = checkout.get('last_name', '').strip()
        
        # O campo 'name' é a concatenação dos dois nomes, como esperado.
        full_name = f"{first_name} {last_name}".strip()
        checkout['name'] = full_name

        # 2. Chama a lógica padrão do Odoo, que agora receberá um campo 'name' preenchido.
        partner_id = super(PartnerDniCheckout, self)._checkout_form_save(mode, checkout, all_form_fields)
        
        # 3. Atualiza os campos personalizados no registo do parceiro.
        partner = request.env['res.partner'].sudo().browse(partner_id)
        if partner:
            partner.write({
                'first_name': first_name,
                'last_name': last_name,
                'dni': checkout.get('dni', '').strip()
            })

        return partner_id
