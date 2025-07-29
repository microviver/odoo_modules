from odoo import http, fields
from odoo.http import request
import logging
from datetime import datetime, timedelta
import random
import string

_logger = logging.getLogger(__name__)

class PopupController(http.Controller):

    @http.route('/newsletter/popup', type='json', auth='public', csrf=False)
    def send_popup_mail(self, email):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if email:
            try:
                nombre = email.split('@')[0]

                # 🔍 Verificar se já existe um código para este email
                discount_code = request.env['popup.discount.code'].sudo().search([('email', '=', email)], limit=1)

                if not discount_code:
                    # ✨ Gerar novo código
                    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                    validade = fields.Date.today() + timedelta(days=7)

                    # 🗃️ Criar registo de desconto
                    discount_code = request.env['popup.discount.code'].sudo().create({
                        'email': email,
                        'code': code,
                        'valid_until': validade
                    })

                    _logger.info(f"{timestamp} odoo.addons.popup_discount.controllers.main: Nuevo código de descuento {code} creado para {email}.")

                else:
                    code = discount_code.code
                    validade = discount_code.valid_until or (fields.Date.today() + timedelta(days=7))

                # ✉️ Criar e enviar email em espanhol
                mail = request.env['mail.mail'].sudo().create({
                    'email_to': email,
                    'email_from': 'tech@microviver.com',
                    'subject': '🎁 ¡Tu código promocional exclusivo!',
                    'body_html': f"""
                        <p>Hola {nombre},</p>
                        <p>¡Gracias por suscribirte!</p>
                        <p>Tu código de descuento es: <strong>{code}</strong></p>
                        <p>Válido hasta: <strong>{validade.strftime('%d/%m/%Y')}</strong></p>
                        <p>Has recibido este correo el: {timestamp}</p>
                    """
                })
                mail.send()

                _logger.info(f"{timestamp} odoo.addons.popup_discount.controllers.main: Código de descuento {code} enviado correctamente a {email}.")

                # 📇 Criar contacto
                contact = request.env['mailing.contact'].sudo().create({
                    'email': email,
                    'name': nombre
                })

                # 🗂️ Associar à lista "Newsletter"
                mailing_list = request.env['mailing.list'].sudo().search([('name', '=', 'Newsletter')], limit=1)
                if mailing_list:
                    mailing_list.write({'contact_ids': [(4, contact.id)]})
                    _logger.info(f"{timestamp} odoo.addons.popup_discount.controllers.main: Contacto {contact.id} añadido a la lista '{mailing_list.name}'.")

                return {'status': 'ok', 'code': code}

            except Exception as e:
                _logger.error(f"{timestamp} odoo.addons.popup_discount.controllers.main: ❌ Error al enviar correo a {email}: {str(e)}")
                return {'status': 'error', 'message': str(e)}

        _logger.warning(f"{timestamp} odoo.addons.popup_discount.controllers.main: ❌ No se proporcionó ningún correo electrónico.")
        return {'status': 'error', 'message': 'No se proporcionó ningún correo electrónico'}

