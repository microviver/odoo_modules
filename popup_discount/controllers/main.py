from odoo import http
from odoo.http import request
import random
import string
import logging

_logger = logging.getLogger(__name__)

class PopupController(http.Controller):

    def _generate_unique_code(self, size=10):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=size))

    @http.route('/newsletter/status', type='json', auth='public', csrf=False)
    def popup_status(self):
        user = request.env.user
        email = user.email if user and not user._is_public() else None
        has_discount = False

        if email:
            has_discount = bool(request.env['popup.discount.code'].sudo().search([('email', '=', email)], limit=1))

        return {
            'logged_in': bool(email),
            'email_registered': has_discount
        }

    @http.route('/newsletter/popup', type='json', auth='public', csrf=False)
    def send_popup_mail(self, email):
        if email:
            try:
                existing = request.env['popup.discount.code'].sudo().search([('email', '=', email)], limit=1)
                if existing:
                    return {'status': 'ok', 'message': 'Código já enviado anteriormente.'}

                code = self._generate_unique_code()
                request.env['popup.discount.code'].sudo().create({
                    'email': email,
                    'code': code,
                })

                body = f"""
                <p>Hola,</p>
                <p>¡Gracias por suscribirte! Aquí tienes tu código exclusivo de 5% de descuento:</p>
                <p style="font-size:20px;text-align:center;"><strong>{code}</strong></p>
                <p>Solo puede ser usado una vez.</p>
                """

                mail = request.env['mail.mail'].sudo().create({
                    'subject': "¡Tu código de descuento!",
                    'email_from': 'info@tutienda.com',
                    'email_to': email,
                    'body_html': body,
                })
                mail.send()

                # Add to mailing list
                mailing_list = request.env['mailing.list'].sudo().search([('name', '=', 'Newsletter')], limit=1)
                if mailing_list:
                    contact = request.env['mailing.contact'].sudo().create({'email': email})
                    mailing_list.write({'contact_ids': [(4, contact.id)]})

                return {'status': 'ok'}
            except Exception as e:
                _logger.error(f"Erro ao enviar email: {e}")
                return {'status': 'error', 'message': str(e)}

        return {'status': 'error', 'message': 'No email provided'}

