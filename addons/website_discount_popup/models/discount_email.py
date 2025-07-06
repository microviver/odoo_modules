from odoo import models, fields

class DiscountEmail(models.Model):
    _name = 'discount.email.coupon'
    _description = 'Email com desconto de popup'

    email = fields.Char(required=True)
    has_discount = fields.Boolean(default=True)
