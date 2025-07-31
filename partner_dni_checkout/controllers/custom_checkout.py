from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleDNI(WebsiteSale):

    @http.route(['/shop/checkout'], type='http', auth="public", website=True, sitemap=False)
    def checkout_form_save(self, **post):
        first_name = post.get('first_name', '').strip()
        last_name = post.get('last_name', '').strip()
        dni_value = post.get('dni', '').strip()

        if not first_name or not last_name or not dni_value:
            return request.redirect('/shop/checkout?error=missing_fields')

        # Combina para preencher o campo padrão 'name'
        post['name'] = f"{first_name} {last_name}"

        response = super().checkout_form_save(**post)

        partner = request.website.sale_get_order().partner_id
        if partner:
            partner.sudo().write({
                'first_name': first_name,
                'last_name': last_name,
                'dni': dni_value
            })

        return response

