from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleInherit(WebsiteSale):

    def checkout(self, **post):
        # Override the checkout method to ensure 'partner' is in the qcontext
        res = super(WebsiteSaleInherit, self).checkout(**post)
        order = res.qcontext['website_sale_order']
        partner = order.partner_id
        res.qcontext['partner'] = partner
        return res
