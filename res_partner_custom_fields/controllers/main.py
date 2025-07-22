from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request

class WebsiteSaleCustom(WebsiteSale):

    def checkout_form_save(self, mode, partner_values, all_values, checkout):
        partner_values['nombre'] = all_values.get('nombre', '')
        partner_values['apelido'] = all_values.get('apelido', '')
        partner_values['dni'] = all_values.get('dni', '')
        return super().checkout_form_save(mode, partner_values, all_values, checkout)

