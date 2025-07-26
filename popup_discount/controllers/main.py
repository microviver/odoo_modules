from odoo import http
from odoo.http import request
import random
import string
import logging

_logger = logging.getLogger(__name__)

class PopupController(http.Controller):

    def _generate_unique_code(self, size=10):
        # Garante que o código é único no banco de dados
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=size))
            if not request.env['popup.discount.code'].sudo().search([('code', '=', code)]):
                return code

    @http.route('/newsletter/status', type='json', auth='public', csrf=False)
    def popup_status(self):
        # Esta rota é mais para debug ou para uma lógica mais avançada de popup
        # No seu caso atual, o localStorage já gerencia a exibição inicial do popup.
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
        if not email:
            return {'status': 'error', 'message': 'E-mail não fornecido.'}

        try:
            # Verifica se o email já tem um código de desconto associado
            existing_code = request.env['popup.discount.code'].sudo().search([('email', '=', email)], limit=1)
            if existing_code:
                _logger.info(f"Email {email} já tem um código de desconto registado.")
                return {'status': 'exists', 'message': 'Código já enviado anteriormente para este e-mail.'}

            code = self._generate_unique_code()  # Usar a função que gera código único

            # Cria o registro do código de desconto
            discount_record = request.env['popup.discount.code'].sudo().create({
                'email': email,
                'code': code,
                'used': False,
            })

            # Envia o e-mail usando o template
            template = request.env.ref('popup_discount.popup_discount_template').sudo()
            if template:
                # Renderiza o corpo do e-mail com o código gerado
                body_html = template._render_template(
                    template.body_html,
                    {'object': discount_record, 'code': code, 'email': email}
                )

                mail_values = {
                    'subject': "¡Tu código de descuento!",
                    'email_from': request.env.user.company_id.email or 'info@tutienda.com',
                    'email_to': email,
                    'body_html': body_html,
                    'model_id': request.env.ref('popup_discount.model_popup_discount_code').id,
                    'res_id': discount_record.id,
                }
                mail = request.env['mail.mail'].sudo().create(mail_values)
                mail.send()
                _logger.info(f"Código de desconto {code} enviado para {email}.")
            else:
                _logger.error("Template de e-mail 'popup_discount_template' não encontrado.")
                return {'status': 'error', 'message': 'Erro ao encontrar template de e-mail.'}

            # Adicionar à lista de e-mails, se desejar
            mailing_list = request.env['mailing.list'].sudo().search([('name', '=', 'Newsletter')], limit=1)
            if not mailing_list:
                mailing_list = request.env['mailing.list'].sudo().create({'name': 'Newsletter'})
                _logger.info("Lista de mailing 'Newsletter' criada.")

            if mailing_list:
                contact = request.env['mailing.contact'].sudo().search([('email', '=', email)], limit=1)
                if not contact:
                    contact = request.env['mailing.contact'].sudo().create({'email': email, 'name': email})

                if contact not in mailing_list.contact_ids:
                    mailing_list.write({'contact_ids': [(4, contact.id)]})
                    _logger.info(f"Email {email} adicionado à lista de mailing 'Newsletter'.")
                else:
                    _logger.info(f"Email {email} já está na lista de mailing 'Newsletter'.")

            return {'status': 'ok'}

        except Exception as e:
            _logger.error(f"Erro ao processar envio de email de desconto para {email}: {e}", exc_info=True)
            request.env.cr.rollback()
            return {'status': 'error', 'message': 'Ocorreu um erro interno. Por favor, tente novamente mais tarde.'}

