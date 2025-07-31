from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class PartnerDniCheckout(WebsiteSale):

    # This method is called by the checkout process to prepare a partner record
    # It's the perfect place to inject custom fields before the partner is created/updated
    def _checkout_form_validate_fields(self, mode, all_form_fields):
        # The parent method handles validation of standard fields
        res = super(PartnerDniCheckout, self)._checkout_form_validate_fields(mode, all_form_fields)
        
        # Here we can add our custom fields to the list of fields to validate
        res.append('first_name')
        res.append('last_name')
        res.append('dni')
        
        return res
    
    def _checkout_form_save(self, mode, checkout, all_form_fields):
        # This method is called to save the checkout data to the partner
        partner_id = super(PartnerDniCheckout, self)._checkout_form_save(mode, checkout, all_form_fields)

        # Get the new partner record to update our custom fields
        partner = request.env['res.partner'].sudo().browse(partner_id)

        if partner:
            # Get the values for our custom fields from the checkout data
            first_name = checkout.get('first_name', '').strip()
            last_name = checkout.get('last_name', '').strip()
            dni_value = checkout.get('dni', '').strip()
            
            # Update the partner record with the new custom fields
            partner.write({
                'first_name': first_name,
                'last_name': last_name,
                'dni': dni_value
            })

        return partner_id
