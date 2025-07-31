from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale


class PartnerDniCheckout(WebsiteSale):

    def _merge_name(self, values):
        """Garante que 'name' seja sempre first_name + last_name."""
        first_name = (values.get('first_name') or "").strip()
        last_name = (values.get('last_name') or "").strip()
        if first_name or last_name:
            values['name'] = (first_name + " " + last_name).strip()
        return values

    @http.route(
        ['/shop/address/submit'],
        type='http', auth="public", methods=['POST'], website=True, sitemap=False
    )
    def checkout_form_validate(self, **post):
        """Intercepta o checkout antes da validação."""
        post = self._merge_name(post)
        return super().checkout_form_validate(**post)

    def address_form_save(self, partner_id, mode, all_values, data):
        """
        Intercepta a gravação de endereços para garantir consistência
        mesmo em edições posteriores feitas pelo usuário.
        """
        all_values = self._merge_name(all_values)
        return super().address_form_save(partner_id, mode, all_values, data)

