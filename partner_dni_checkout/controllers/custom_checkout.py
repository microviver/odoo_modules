from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class PartnerDniCheckout(WebsiteSale):

    @http.route(
        ['/shop/address/submit'], # This is the correct route for the address form submission
        type='http', auth="public", methods=['POST'], website=True, sitemap=False
    )
    def checkout_form_validate(self, **post):
        # Call the original method first.
        # This handles Odoo's default validation for standard fields (including 'name' from your hidden input)
        # and proceeds to the next step or re-renders the page with errors.
        response = super(PartnerDniCheckout, self).checkout_form_validate(**post)

        # After the super call, if an order and partner are successfully associated,
        # update the custom fields.
        order = request.website.sale_get_order()
        partner = order.partner_id if order else None

        if partner:
            # Get the values for your custom fields from the post data
            first_name = post.get('first_name', '').strip()
            last_name = post.get('last_name', '').strip()
            dni_value = post.get('dni', '').strip()

            # Update the partner record with the new custom fields
            # Use .sudo() to ensure you have the necessary permissions to write
            partner.sudo().write({
                'first_name': first_name,
                'last_name': last_name,
                'dni': dni_value
            })

        # Return the response from the original method.
        # This will either be a redirect to the next step (e.g., payment)
        # or the current page with validation errors.
        return response
