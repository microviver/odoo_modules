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
            _logger.warning("Email não fornecido para o popup de desconto.")
            return {'status': 'error', 'message': 'E-mail não fornecido.'}

        try:
            # Check for existing code
            existing_code = request.env['popup.discount.code'].sudo().search([('email', '=', email)], limit=1)
            if existing_code:
                _logger.info(f"Email {email} já tem um código de desconto registado. Código: {existing_code.code}")
                return {'status': 'exists', 'message': f'Código {existing_code.code} já enviado anteriormente para este e-mail.'}

            # Generate and create new code
            code = self._generate_unique_code()
            discount_record = request.env['popup.discount.code'].sudo().create({
                'email': email,
                'code': code,
                'used': False,
            })
            _logger.info(f"Novo código de desconto {code} criado para {email}.")

            # Get email template
            template = request.env.ref('popup_discount.popup_discount_template').sudo()
            if not template:
                _logger.error("Template de e-mail 'popup_discount_template' não encontrado.")
                return {'status': 'error', 'message': 'Erro ao encontrar template de e-mail.'}

            # Render email body - METHOD 1: Using template.send_mail() - RECOMMENDED
            try:
                template.with_context(
                    object=discount_record,
                    code=code,
                    email=email
                ).send_mail(discount_record.id, force_send=True)
                
                _logger.info(f"Código de desconto {code} enviado com sucesso para {email}.")
                return {'status': 'ok'}
            
            except Exception as e:
                _logger.error(f"Falha ao enviar email via template: {e}")
                # Fallback to manual method if template sending fails

            # METHOD 2: Manual email composition (fallback)
            try:
                # Render body using qweb
                body_html = request.env['ir.qweb'].sudo()._render(
                    'popup_discount.email_template_discount_code',
                    {
                        'object': discount_record,
                        'code': code,
                        'email': email
                    }
                )
                
                mail_values = {
                    'subject': template.subject or "¡Tu código de descuento exclusivo está aquí!",
                    'email_from': template.email_from or 'tech@microviver.com',
                    'email_to': email,
                    'body_html': body_html,
                    'model': 'popup.discount.code',
                    'res_id': discount_record.id,
                }
                
                _logger.info(f"Preparando para enviar email manualmente para {email}")
                mail = request.env['mail.mail'].sudo().create(mail_values)
                mail.send()
                _logger.info(f"Código de desconto {code} enviado com sucesso para {email}.")
                return {'status': 'ok'}
                
            except Exception as fallback_e:
                _logger.error(f"Falha no método alternativo de envio: {fallback_e}")
                raise fallback_e

        except Exception as e:
            _logger.error(f"Erro ao processar envio de email de desconto para {email}: {e}", exc_info=True)
            request.env.cr.rollback()
            return {'status': 'error', 'message': f'Ocorreu um erro interno: {e}. Por favor, tente novamente mais tarde.'}
