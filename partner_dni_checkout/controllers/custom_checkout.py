from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class PartnerDniCheckout(WebsiteSale):

    @http.route(['/shop/checkout'], type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def checkout(self, **post):
        # Juntar first_name + last_name em name para compatibilidade com o core
        first_name = post.get('first_name', '').strip()
        last_name = post.get('last_name', '').strip()
        full_name = (first_name + ' ' + last_name).strip()

        # Atualiza o parâmetro post com 'name'
        post = post.copy()
        post['name'] = full_name

        # Chama o método original com o post atualizado
        return super(PartnerDniCheckout, self).checkout(**post)

