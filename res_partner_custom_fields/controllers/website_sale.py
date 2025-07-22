from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleInherit(WebsiteSale):
    
    @http.route()
    def address(self, **kw):
        """Override address method to handle DNI field"""
        response = super().address(**kw)
        
        # Handle DNI field in form submission
        if request.httprequest.method == 'POST' and 'submitted' in kw:
            partner_id = request.session.get('partner_id')
            if partner_id and 'dni' in kw:
                partner = request.env['res.partner'].browse(partner_id)
                partner.sudo().write({'dni': kw.get('dni', '')})
        
        return response
    
    def _get_mandatory_fields_billing(self, country_id=False):
        """Add DNI to mandatory fields if needed"""
        mandatory_fields = super()._get_mandatory_fields_billing(country_id)
        # Uncomment next line if you want DNI to be mandatory
        # mandatory_fields.append('dni')
        return mandatory_fields
    
    def _get_mandatory_fields_shipping(self, country_id=False):
        """Add DNI to mandatory shipping fields if needed"""
        mandatory_fields = super()._get_mandatory_fields_shipping(country_id)
        # Uncomment next line if you want DNI to be mandatory for shipping
        # mandatory_fields.append('dni')
        return mandatory_fields

