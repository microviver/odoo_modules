from odoo import models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        order = super().create(vals)
        code = vals.get('client_order_ref')
        if code:
            record = self.env['popup.discount.code'].sudo().search([
                ('code', '=', code),
                ('used', '=', False)
            ], limit=1)
            if record:
                discount = order.amount_total * 0.05
                order.write({'amount_total': order.amount_total - discount})
                record.write({'used': True})
        return order

