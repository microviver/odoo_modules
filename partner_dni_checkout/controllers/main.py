from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleInherit(WebsiteSale):

    # Mantemos o método checkout para garantir que 'checkout' esteja no contexto.
    # Isso resolve o KeyError que você estava a ter.
    @http.route(['/shop/checkout'], type='http', auth="public", website=True, sitemap=False)
    def checkout(self, **post):
        res = super(WebsiteSaleInherit, self).checkout(**post)
        if 'checkout' not in res.qcontext:
            res.qcontext['checkout'] = {}
        return res

    def checkout_form_save(self, checkout, **kw):
        """ Salva last_name e dni no res.partner """
        # Remove a lógica de first_name
        if kw.get('last_name'):
            checkout['last_name'] = kw.get('last_name').strip()
        if kw.get('dni'):
            checkout['dni'] = kw.get('dni').strip()
        
        # A combinação do nome será feita no modelo, então não é
        # necessário fazer a concatenação aqui.
        
        return super().checkout_form_save(checkout, **kw)
