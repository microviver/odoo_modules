from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request

class WebsiteSaleCustom(WebsiteSale):

    def _get_partner_values(self, data):
        values = super()._get_partner_values(data)
        values['firstname'] = data.get('firstname')
        values['lastname'] = data.get('lastname')
        values['dni'] = data.get('dni')
        values['name'] = f"{data.get('firstname', '')} {data.get('lastname', '')}"
        return values
