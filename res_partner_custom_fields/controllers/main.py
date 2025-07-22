from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request
from odoo import http

class WebsiteSaleCustom(WebsiteSale):

    def checkout_form_save(self, mode, partner_values, all_values, checkout):
        # Captura os campos personalizados enviados no /shop/address
        if 'nombre' in all_values:
            partner_values['nombre'] = all_values['nombre']
        if 'apelido' in all_values:
            partner_values['apelido'] = all_values['apelido']
        if 'dni' in all_values:
            partner_values['dni'] = all_values['dni']
        return super().checkout_form_save(mode, partner_values, all_values, checkout)

