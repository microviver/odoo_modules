# controllers/main.py
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request

class WebsiteSaleInherit(WebsiteSale):

    def checkout_form_save(self, checkout):
        if 'x_dni' in checkout:
            request.session['partner_id'] = request.env['res.partner'].sudo().browse(
                request.session.get('partner_id')
            ).write({'x_dni': checkout.get('x_dni')})
        return super().checkout_form_save(checkout)

