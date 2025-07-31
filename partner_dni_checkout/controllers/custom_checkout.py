from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class PartnerDniCheckout(WebsiteSale):

    # Este método é chamado para guardar os dados do formulário no parceiro
    # Vamos usá-lo para garantir que o campo 'name' final é preenchido corretamente
    def _checkout_form_save(self, mode, checkout, all_form_fields):
        # 1. Obter os valores submetidos para 'name' e 'last_name'
        submitted_name = checkout.get('name', '').strip()
        last_name = checkout.get('last_name', '').strip()

        # 2. Concatenar 'name' e 'last_name' para o campo final 'name'
        if last_name:
            full_name = f"{submitted_name} {last_name}".strip()
            checkout['name'] = full_name
        else:
            checkout['name'] = submitted_name

        # 3. Chama a lógica padrão do Odoo, que agora receberá um campo 'name' preenchido.
        partner_id = super(PartnerDniCheckout, self)._checkout_form_save(mode, checkout, all_form_fields)
        
        # 4. Atualiza os campos personalizados no registo do parceiro.
        partner = request.env['res.partner'].sudo().browse(partner_id)
        if partner:
            partner.write({
                'last_name': last_name, # Guarda o apelido no campo personalizado
                'dni': checkout.get('dni', '').strip() # Guarda o DNI
            })

        return partner_id
