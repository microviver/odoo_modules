from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class PartnerDniCheckout(WebsiteSale):

    # Método para garantir que os dados do formulário persistam
    # após uma validação falhada.
    def _get_checkout_data(self, **kw):
        # Chama a lógica original para obter o dicionário de dados padrão
        res = super(PartnerDniCheckout, self)._get_checkout_data(**kw)

        # Adiciona os dados do formulário submetido (request.params)
        # ao dicionário 'checkout' do Odoo.
        # Isto garante que os campos personalizados são repovoados no formulário
        # após um erro de validação.
        res['checkout'].update(request.params)
        
        return res

    # Este método é responsável por guardar os dados no parceiro.
    # Já o tinha, mas foi ajustado para usar 'checkout' em vez de 'post'.
    def _checkout_form_save(self, mode, checkout, all_form_fields):
        # A super-chamada faz a lógica padrão do Odoo, criando/atualizando o parceiro
        # e preenchendo o campo 'name' com a concatenação.
        partner_id = super(PartnerDniCheckout, self)._checkout_form_save(mode, checkout, all_form_fields)
        
        # Agora, atualizamos o parceiro com os nossos campos personalizados.
        partner = request.env['res.partner'].sudo().browse(partner_id)
        if partner:
            partner.write({
                'first_name': checkout.get('first_name', '').strip(),
                'last_name': checkout.get('last_name', '').strip(),
                'dni': checkout.get('dni', '').strip()
            })

        return partner_id
