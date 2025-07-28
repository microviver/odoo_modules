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
                nome = email.split('@')[0]

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

                    _logger.info(f"{timestamp} odoo.addons.popup_discount.controllers.main: Novo código de desconto {code} criado para {email}.")

                else:
                    code = discount_code.code
                    validade = discount_code.valid_until or (fields.Date.today() + timedelta(days=7))

                # ✉️ Criar e enviar email
                mail = request.env['mail.mail'].sudo().create({
                    'email_to': email,
                    'email_from': 'tech@microriver.com',
                    'subject': '🎁 O teu código promocional exclusivo!',
                    'body_html': f"""
                        <p>Olá {nome},</p>
                        <p>Obrigado por te inscreveres!</p>
                        <p>O teu código de desconto é: <strong>{code}</strong></p>
                        <p>Válido até: <strong>{validade.strftime('%d/%m/%Y')}</strong></p>
                        <p>Recebeste este email em: {timestamp}</p>
                    """
                })
                mail.send()

                _logger.info(f"{timestamp} odoo.addons.popup_discount.controllers.main: Código de desconto {code} enviado com sucesso para {email}.")

                # 📇 Criar contacto
                contact = request.env['mailing.contact'].sudo().create({
                    'email': email,
                    'name': nome
                })

                # 🗂️ Associar à lista "Newsletter"
                mailing_list = request.env['mailing.list'].sudo().search([('name', '=', 'Newsletter')], limit=1)
                if mailing_list:
                    mailing_list.write({'contact_ids': [(4, contact.id)]})
                    _logger.info(f"{timestamp} odoo.addons.popup_discount.controllers.main: Contacto {contact.id} adicionado à lista '{mailing_list.name}'.")

                return {'status': 'ok', 'code': code}

            except Exception as e:
                _logger.error(f"{timestamp} odoo.addons.popup_discount.controllers.main: ❌ Erro ao enviar email para {email}: {str(e)}")
                return {'status': 'error', 'message': str(e)}

        _logger.warning(f"{timestamp} odoo.addons.popup_discount.controllers.main: ❌ Nenhum email fornecido.")
        return {'status': 'error', 'message': 'No email provided'}

