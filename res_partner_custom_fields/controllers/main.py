class WebsiteSaleCustom(WebsiteSale):
    @http.route(['/shop/address'], type='http', auth="public", website=True, sitemap=False)
    def address(self, **kw):
        response = super().address(**kw)
        if 'partner_id' in kw:
            partner = request.env['res.partner'].browse(int(kw['partner_id']))
            response.qcontext['partner'].update({
                'nombre': partner.nombre or '',
                'apellido': partner.apellido or '',
                'dni': partner.dni or '',
            })
        return response
