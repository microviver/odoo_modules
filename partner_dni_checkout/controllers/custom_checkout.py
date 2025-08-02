from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale

class PartnerDniCheckout(WebsiteSale):

    def _merge_name(self, values):
        """
        Garante que o campo 'name' do Odoo (para o parceiro) seja a concatenação
        do que o usuário digitou no campo 'Nome' (o 'name' do formulário)
        e no campo 'Apelido' (o 'last_name' do formulário).
        """
        # Pega o valor atual do campo 'name' do formulário (que agora é o 'Nome')
        # e o valor do campo 'last_name' (o 'Apelido').
        form_name_value = (values.get('name') or "").strip()
        form_last_name_value = (values.get('last_name') or "").strip()

        # Concatena os dois valores para formar o 'name' final do parceiro.
        # Isso garante que o campo 'name' no res.partner contenha 'Nome Sobrenome'.
        if form_name_value or form_last_name_value:
            values['name'] = (form_name_value + " " + form_last_name_value).strip()
        
        # Importante: O Odoo salva o campo 'name' do formulário como o 'name' do res.partner.
        # Se você tiver um campo 'last_name' customizado no modelo res.partner,
        # ele será salvo separadamente pelo seu _checkout_form_save (se tiver um,
        # ou precisará de uma adaptação similar ao que discutimos antes para salvar o DNI).
        # Este _merge_name foca em como o 'name' principal do parceiro é formado.

        return values

    @http.route(
        ['/shop/address/submit'],
        type='http', auth="public", methods=['POST'], website=True, sitemap=False
    )
    def checkout_form_validate(self, **post):
        """Intercepta o checkout antes da validação para ajustar o 'name'."""
        post = self._merge_name(post)
        return super().checkout_form_validate(**post)

    def address_form_save(self, partner_id, mode, all_values, data):
        """
        Intercepta a gravação de endereços para garantir consistência
        mesmo em edições posteriores feitas pelo usuário, ajustando o 'name'.
        """
        all_values = self._merge_name(all_values)
        
        # Além de ajustar o 'name', precisamos garantir que o 'last_name'
        # e o 'dni' customizados sejam salvos no res.partner.
        # O 'all_values' já conterá 'last_name' e 'dni' do formulário.
        # Precisamos aplicar isso ao parceiro.

        res = super().address_form_save(partner_id, mode, all_values, data)
        
        # Agora, salve os campos customizados 'last_name' e 'dni' no parceiro.
        # Você precisará ter certeza de que 'request' está importado se ainda não estiver,
        # ou se o 'address_form_save' da superclasse já não lida com isso.
        # Para ser seguro e explícito:
        from odoo.http import request # Adicione esta importação se ainda não a tiver

        partner = request.env['res.partner'].sudo().browse(partner_id)
        if partner.exists():
            partner.write({
                'last_name': all_values.get('last_name', '').strip(),
                'dni': all_values.get('dni', '').strip()
            })
        return res
