from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale


class PartnerDniCheckout(WebsiteSale):

    @http.route(
        ['/shop/address/submit'],
        type='http', auth="public", methods=['POST'], website=True, sitemap=False
    )
    def address_form_validate(self, mode, all_values, data):
        """
        Sobrescreve a validação do formulário de endereço no checkout.
        Junta first_name + last_name em 'name' antes da validação.
        """
        # Garantir que não quebre se os campos não existirem
        first_name = (data.get('first_name') or "").strip()
        last_name = (data.get('last_name') or "").strip()

        # Substituir o campo name pela junção
        if first_name or last_name:
            data['name'] = (first_name + " " + last_name).strip()

        # Continua o fluxo original de validação
        return super().address_form_validate(mode, all_values, data)

