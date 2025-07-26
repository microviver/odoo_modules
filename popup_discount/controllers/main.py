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
        # Implemente a lógica aqui para determinar se o popup deve ser exibido.
        # Por exemplo, verificar se o usuário já tem um código, etc.
        # Por enquanto, vamos sempre mostrar para teste.
        return {'can_show': True}

    @http.route('/newsletter/popup', type='json', auth='public', csrf=False)
    def send_popup_mail(self, email):
        if not email:
            _logger.warning("Email não fornecido para o popup de desconto.")
            return {'status': 'error', 'message': 'E-mail não fornecido.'}

        try:
            # Verifica se o email já tem um código de desconto associado
            existing_code = request.env['popup.discount.code'].sudo().search([('email', '=', email)], limit=1)
            if existing_code:
                _logger.info(f"Email {email} já tem um código de desconto registado. Código: {existing_code.code}")
                # Reenviar o código existente caso já tenha sido enviado e a lógica do popup decida isso.
                # Ou apenas informar que já existe.
                return {'status': 'exists', 'message': f'Código {existing_code.code} já enviado anteriormente para este e-mail.'}

            code = self._generate_unique_code() # Gera o novo código único
            
            # Cria o registro do código de desconto
            discount_record = request.env['popup.discount.code'].sudo().create({
                'email': email,
                'code': code,
                'used': False,
            })
            _logger.info(f"Novo código de desconto {code} criado para {email}.")

            # Envia o e-mail usando o template
            # IMPORTANTE: Use .sudo() para acessar o template de e-mail com permissões elevadas
            template = request.env.ref('popup_discount.popup_discount_template').sudo() 
            if template:
                # Renderiza o corpo do e-mail com o código gerado
                # Passe o 'object' para que o template possa usar ${object.code}
                # CORREÇÃO AQUI: Adicionar [discount_record.id] como segundo argumento para _render_template
                body_html = template._render_template(
                    template.body_html,
                    [discount_record.id], # <<-- NOVO ARGUMENTO AQUI
                    {'object': discount_record, 'code': code, 'email': email}
                )
                 
                mail_values = {
                    'subject': "¡Tu código de descuento exclusivo está aquí!",
                    'email_from': 'tech@microviver.com', # Pode ser dinâmico ou fixo como agora
                    'email_to': email,
                    'body_html': body_html,
                    'model_id': request.env.ref('popup_discount.model_popup_discount_code').id, # Associa ao modelo de códigos
                    'res_id': discount_record.id, # Associa ao registro do código específico
                }
                _logger.info(f"Preparando para enviar email para {email} com assunto: {mail_values['subject']}")
                mail = request.env['mail.mail'].sudo().create(mail_values)
                mail.send()
                _logger.info(f"Código de desconto {code} enviado com sucesso para {email}.")
            else:
                _logger.error("Template de e-mail 'popup_discount_template' não encontrado.")
                return {'status': 'error', 'message': 'Erro ao encontrar template de e-mail.'}

            # Lógica para adicionar à lista de marketing (se aplicável)
            # if request.env.ref('mailing.mailing_list_1', False): # Substitua pelo ID externo da sua mailing list
            #     mailing_list = request.env.ref('mailing.mailing_list_1').sudo()
            #     request.env['mailing.contact'].sudo().create({
            #         'name': email,
            #         'email': email,
            #         'subscription_list_ids': [(4, mailing_list.id)],
            #     })
            #     _logger.info(f"Email {email} adicionado à lista de marketing.")

            return {'status': 'ok'}

        except Exception as e:
            _logger.error(f"Erro ao processar envio de email de desconto para {email}: {e}", exc_info=True)
            request.env.cr.rollback() # Garante rollback em caso de erro no banco de dados
            return {'status': 'error', 'message': f'Ocorreu um erro interno: {e}. Por favor, tente novamente mais tarde.'}
