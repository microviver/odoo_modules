from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request

class WebsiteSaleCustom(WebsiteSale):

    def checkout_form_save(self, mode, partner_values, all_values, checkout):
        partner_values['nombre'] = all_values.get('nombre', '')
        partner_values['apellido'] = all_values.get('apellido', '')
        partner_values['dni'] = all_values.get('dni', '')
        return super().checkout_form_save(mode, partner_values, all_values, checkout)

    @http.route(['/shop/checkout'], type='http', auth="public", website=True, sitemap=False)
    def checkout(self, **post):
        response = super().checkout(**post)
        order = request.website.sale_get_order()
        if order:
            partner = order.partner_id
            post.update({
                'nombre': partner.nombre or '',
                'apellido': partner.apellido or '',
                'dni': partner.dni or '',
            })
        return response

