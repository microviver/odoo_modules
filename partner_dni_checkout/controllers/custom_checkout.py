from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class PartnerDniCheckout(WebsiteSale):

    # Sobrescrevemos o método que renderiza a página de endereço para garantir
    # que o dicionário `checkout` está sempre presente.
    @http.route('/shop/address', type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def checkout_address(self, **kw):
        response = super(PartnerDniCheckout, self).checkout_address(**kw)

        # Se a resposta for um dicionário (o que significa que vai renderizar um template),
        # garantimos que o dicionário `checkout` está presente e populado.
        if isinstance(response, dict):
            checkout = response.setdefault('checkout', {})
            checkout.update(request.params)
            
            # Adicionamos aqui a lógica de preenchimento do nome completo
            submitted_name = checkout.get('name', '').strip()
            last_name = checkout.get('last_name', '').strip()
            full_name = f"{submitted_name} {last_name}".strip()
            checkout['name'] = full_name

        return response

    # Este método é chamado para guardar os dados do formulário no parceiro
    # A lógica de concatenação do nome foi movida para o checkout_address acima
    def _checkout_form_save(self, mode, checkout, all_form_fields):
        # A super-chamada irá agora usar o campo 'name' já corrigido no dicionário `checkout`
        partner_id = super(PartnerDniCheckout, self)._checkout_form_save(mode, checkout, all_form_fields)
        
        # Atualizamos apenas os campos personalizados no registo do parceiro.
        partner = request.env['res.partner'].sudo().browse(partner_id)
        if partner:
            partner.write({
                'last_name': checkout.get('last_name', '').strip(),
                'dni': checkout.get('dni', '').strip()
            })

        return partner_id
