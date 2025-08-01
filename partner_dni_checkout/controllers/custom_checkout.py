from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class PartnerDniCheckout(WebsiteSale):

    # Odoo 18.0 usa o método `checkout` para lidar com a rota /shop/address.
    # Iremos sobrescrevê-lo para injetar a nossa lógica de preenchimento dos campos.
    @http.route(['/shop/address'], type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def checkout(self, **post):
        # A super-chamada irá executar a lógica padrão do checkout do Odoo.
        response = super(PartnerDniCheckout, self).checkout(**post)
        
        # A resposta pode ser um dicionário (para renderizar um template)
        # ou uma resposta de redirecionamento.
        if isinstance(response, dict):
            # Se for um dicionário, garantimos que a variável 'checkout' existe
            # e a preenchemos com os dados submetidos no formulário (POST)
            # para que os campos não fiquem vazios após um erro de validação.
            checkout_data = response.setdefault('checkout', {})
            checkout_data.update(post)

            # Aqui, implementamos a sua lógica de concatenação do nome.
            # O nome completo é criado a partir de 'name' e 'last_name' do formulário
            # e colocado de volta no dicionário `checkout` para ser usado na próxima etapa.
            submitted_name = checkout_data.get('name', '').strip()
            last_name = checkout_data.get('last_name', '').strip()
            
            if last_name:
                full_name = f"{submitted_name} {last_name}".strip()
                checkout_data['name'] = full_name
            else:
                checkout_data['name'] = submitted_name
        
        return response

    # O método `_checkout_form_save` é chamado internamente e é o local
    # correto para guardar os campos personalizados no modelo res.partner.
    def _checkout_form_save(self, mode, checkout, all_form_fields):
        # A super-chamada irá usar o campo 'name' já corrigido no método acima.
        partner_id = super(PartnerDniCheckout, self)._checkout_form_save(mode, checkout, all_form_fields)
        
        # Atualizamos os campos personalizados no registo do parceiro.
        partner = request.env['res.partner'].sudo().browse(partner_id)
        if partner:
            partner.write({
                'last_name': checkout.get('last_name', '').strip(),
                'dni': checkout.get('dni', '').strip()
            })

        return partner_id
