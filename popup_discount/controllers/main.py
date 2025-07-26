import logging
from odoo import http
from odoo.http import request
import random
import string

_logger = logging.getLogger(__name__)

class PopupController(http.Controller):

    def _generate_unique_code(self, size=10):
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=size))
            if not request.env['popup.discount.code'].sudo().search([('code', '=', code)]):
                return code

    @http.route('/newsletter/popup_status', type='json', auth='public', csrf=False)
    def popup_status(self):
        return {'can_show': True}

    @http.route('/newsletter/popup', type='json', auth='public', csrf=False)
    def send_popup_mail(self, email):
        if not email:
            return {
                'status': 'error',
                'message': 'Por favor, insira um endereço de email válido.',
                'alert_type': 'error'
            }

        try:
            # Verificar se o email já tem um código
            existing_code = request.env['popup.discount.code'].sudo().search([('email', '=', email)], limit=1)
            if existing_code:
                return {
                    'status': 'exists',
                    'message': f'Você já recebeu um código anteriormente: {existing_code.code}',
                    'alert_type': 'warning'
                }

            # Gerar novo código
            code = self._generate_unique_code()
            discount_record = request.env['popup.discount.code'].sudo().create({
                'email': email,
                'code': code,
                'used': False,
            })

            # Enviar email
            template = request.env.ref('popup_discount.popup_discount_template').sudo()
            if template:
                template.with_context(code=code).send_mail(discount_record.id, force_send=True)
                
                # Verificar se o email foi realmente enviado
                mail = request.env['mail.mail'].sudo().search([
                    ('model', '=', 'popup.discount.code'),
                    ('res_id', '=', discount_record.id)
                ], limit=1)
                
                if mail and mail.state == 'sent':
                    return {
                        'status': 'ok',
                        'message': 'Código enviado com sucesso! Por favor verifique sua caixa de entrada.',
                        'alert_type': 'success'
                    }
                else:
                    return {
                        'status': 'error',
                        'message': 'Email não pôde ser enviado. Por favor tente novamente mais tarde.',
                        'alert_type': 'error'
                    }
            else:
                return {
                    'status': 'error',
                    'message': 'Erro de configuração. Por favor contate o suporte.',
                    'alert_type': 'error'
                }

        except Exception as e:
            _logger.error(f"Erro ao enviar código de desconto: {str(e)}", exc_info=True)
            return {
                'status': 'error',
                'message': 'Ocorreu um erro inesperado. Por favor tente novamente.',
                'alert_type': 'error'
            }
