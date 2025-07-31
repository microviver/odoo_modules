from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class PartnerDniCheckout(WebsiteSale):

    @http.route(
        ['/shop/address/submit'],
        type='http', auth="public", methods=['POST'], website=True, sitemap=False
    )
    def checkout_form_validate(self, **post):
        # Passo 1: Juntar first_name + last_name em name.
        # Isso garante que a validação do Odoo tenha o campo 'name' preenchido corretamente.
        first_name = post.get('first_name', '').strip()
        last_name = post.get('last_name', '').strip()
        post['name'] = (first_name + ' ' + last_name).strip()

        # Passo 2: Chamar o método original do Odoo para a validação.
        # O método 'super' irá agora processar o 'post' data modificado.
        # A resposta será o formulário recarregado com o erro ou o redirecionamento para o próximo passo.
        response = super(PartnerDniCheckout, self).checkout_form_validate(**post)

        return response

