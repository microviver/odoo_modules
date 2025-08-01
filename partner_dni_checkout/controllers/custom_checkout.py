from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class PartnerDniCheckout(WebsiteSale):

    @http.route(['/shop/address'], type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def checkout(self, **post):
        # Chamada direta ao método original da classe base
        response = WebsiteSale.checkout(self, **post)

        if isinstance(response, dict):
            checkout_data = response.setdefault('checkout', {})
            checkout_data.update(post)

            # Concatenação do nome completo
            first_name = checkout_data.get('name', '').strip()
            last_name = checkout_data.get('last_name', '').strip()

            full_name = f"{first_name} {last_name}".strip() if last_name else first_name
            checkout_data['name'] = full_name

        return response

    def _checkout_form_save(self, mode, checkout, all_form_fields):
        # Chamada ao método original para salvar os dados padrão
        partner_id = super()._checkout_form_save(mode, checkout, all_form_fields)

        # Atualização dos campos personalizados
        partner = request.env['res.partner'].sudo().browse(partner_id)
        if partner.exists():
            partner.write({
                'last_name': checkout.get('last_name', '').strip(),
                'dni': checkout.get('dni', '').strip()
            })

        return partner_id

