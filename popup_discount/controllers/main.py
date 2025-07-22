from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class PopupController(http.Controller):

    @http.route('/newsletter/popup', type='json', auth='public', csrf=False)
    def send_popup_mail(self, email):
        if email:
            try:
                # Usar o template de email com o nome técnico correto
                template = request.env.ref('popup_discount.popup_discount_template')
                template.send_mail(
                    res_id=None,
                    email_to=email,
                    force_send=True
                )

                # Criar contacto na lista de marketing (opcional)
                contact = request.env['mailing.contact'].sudo().create({
                    'email': email,
                    'name': email.split('@')[0]
                })

                # Adicionar a lista "Newsletter" (ou outro nome que escolheres)
                mailing_list = request.env['mailing.list'].sudo().search([('name', '=', 'Newsletter')], limit=1)
                if mailing_list:
                    mailing_list.write({'contact_ids': [(4, contact.id)]})

                return {'status': 'ok'}
            except Exception as e:
                _logger.error(f"Erro ao enviar email de popup: {str(e)}")
                return {'status': 'error', 'message': str(e)}

        return {'status': 'error', 'message': 'No email provided'}

