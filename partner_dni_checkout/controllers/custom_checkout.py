from odoo import http
from odoo.http import request # Importar request é crucial
from odoo.addons.website_sale.controllers.main import WebsiteSale

class PartnerDniCheckout(WebsiteSale):

    # Este método é o ponto correto para injetar dados no dicionário 'checkout'
    # que será usado pelo template website_sale.address.
    def _get_checkout_values(self, **kw):
        """
        Extende os valores do checkout, garantindo que o dicionário 'checkout' exista
        e contenha os dados necessários para renderização do formulário.
        """
        # Chama o _get_checkout_values da superclasse para obter os valores padrão
        res = super(PartnerDniCheckout, self)._get_checkout_values(**kw)

        # Garante que o dicionário 'checkout' exista em 'res'
        if 'checkout' not in res:
            res['checkout'] = {}

        # Atualiza o dicionário 'checkout' com quaisquer dados POST que venham
        # (por exemplo, se o usuário voltar para a página após um erro de validação)
        res['checkout'].update(kw)

        # Lógica para pre-popular os campos do formulário com base nos dados existentes
        # ou nos dados enviados.
        partner = request.env.user.partner_id
        order = request.website.sale_get_order()

        # Popula 'name', 'last_name' e 'dni' para exibição inicial no formulário
        # Se 'checkout' já tiver valores (ex: de um POST anterior), use-os.
        # Caso contrário, use os dados do parceiro ou do pedido.
        if 'name' not in res['checkout'] and partner:
            # Se o partner.name já contiver "Nome Sobrenome", separe para pre-popular
            if partner.name and ' ' in partner.name.strip():
                parts = partner.name.strip().split(' ', 1) # Divide no primeiro espaço
                res['checkout']['name'] = parts[0]
                res['checkout']['last_name'] = parts[1] if len(parts) > 1 else ''
            else:
                res['checkout']['name'] = partner.name or ''
                res['checkout']['last_name'] = partner.last_name or '' # Pega do seu campo customizado
        
        if 'dni' not in res['checkout'] and partner:
            res['checkout']['dni'] = partner.dni or '' # Pega do seu campo customizado

        # Aplica a lógica de _merge_name para garantir que 'name' tenha o valor concatenado
        # para a parte de validação/gravação, se necessário.
        # Mas para a renderização, é melhor ter o 'name' e 'last_name' separados.
        # A lógica de concatenação será feita nos métodos de salvamento/validação.
        
        return res

    def _merge_name(self, values):
        """Garante que 'name' seja sempre first_name + last_name."""
        # 'name' virá do input com name="name" (label Nome)
        # 'last_name' virá do input com name="last_name" (label Apelido)
        form_first_name = (values.get('name') or "").strip()
        form_last_name = (values.get('last_name') or "").strip()

        # Concatena para formar o valor final do campo 'name' no res.partner
        if form_first_name or form_last_name:
            values['name'] = (form_first_name + " " + form_last_name).strip()
        
        return values

    @http.route(
        ['/shop/address/submit'],
        type='http', auth="public", methods=['POST'], website=True, sitemap=False
    )
    def checkout_form_validate(self, **post):
        """Intercepta o checkout antes da validação."""
        # Aplica a lógica de fusão do nome antes da validação da superclasse
        post = self._merge_name(post)
        return super().checkout_form_validate(**post)

    def address_form_save(self, partner_id, mode, all_values, data):
        """
        Intercepta a gravação de endereços para garantir consistência
        mesmo em edições posteriores feitas pelo usuário.
        """
        # Aplica a lógica de fusão do nome antes de chamar o método de salvamento da superclasse
        all_values = self._merge_name(all_values)
        
        res = super().address_form_save(partner_id, mode, all_values, data)
        
        # Salva os campos customizados 'last_name' e 'dni'
        partner = request.env['res.partner'].sudo().browse(partner_id)
        if partner.exists():
            partner.write({
                'last_name': all_values.get('last_name', '').strip(),
                'dni': all_values.get('dni', '').strip()
            })
        return res
