from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class PartnerDniCheckout(WebsiteSale):

    @http.route(['/shop/address'], type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def address(self, **kw):
        response = super(PartnerDniCheckout, self).address(**kw)
        
        if isinstance(response, str):
            return response
            
        # Ensure checkout dict exists in response
        if 'checkout' not in response:
            response['checkout'] = {}
            
        # Update with posted data
        response['checkout'].update(kw)
        
        # Handle name concatenation
        first_name = response['checkout'].get('name', '').strip()
        last_name = response['checkout'].get('last_name', '').strip()
        full_name = f"{first_name} {last_name}".strip() if last_name else first_name
        response['checkout']['name'] = full_name
        
        return response

    def _checkout_form_save(self, mode, checkout, all_form_fields):
        partner_id = super(PartnerDniCheckout, self)._checkout_form_save(mode, checkout, all_form_fields)
        
        partner = request.env['res.partner'].sudo().browse(partner_id)
        if partner.exists():
            partner.write({
                'last_name': checkout.get('last_name', '').strip(),
                'dni': checkout.get('dni', '').strip()
            })
            
        return partner_id
