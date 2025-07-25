from odoo import models, fields

class PopupDiscountCode(models.Model):
    _name = 'popup.discount.code'
    _description = 'Popup Discount Code'

    email = fields.Char(required=True)
    code = fields.Char(required=True)
    used = fields.Boolean(default=False)

