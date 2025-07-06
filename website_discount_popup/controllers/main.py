from odoo import http
from odoo.http import request

class DiscountPopup(http.Controller):

    @http.route(['/discount_popup/submit'], type='json', auth='public', website=True, csrf=False)
    def submit_email(self, email):
        if email:
            request.env['discount.email.coupon'].sudo().create({'email': email})
            request.session['has_discount'] = True
            return {'success': True}
        return {'success': False, 'error': 'Missing email'}
