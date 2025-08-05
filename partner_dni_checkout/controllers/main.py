from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleInherit(WebsiteSale):

    def checkout_form_save(self, checkout, **kw):
        """ Salva também first_name, last_name e dni no res.partner """
        if kw.get('first_name'):
            checkout['first_name'] = kw.get('first_name').strip()
        if kw.get('last_name'):
            checkout['last_name'] = kw.get('last_name').strip()
        if kw.get('dni'):
            checkout['dni'] = kw.get('dni').strip()

        return super().checkout_form_save(checkout, **kw)

