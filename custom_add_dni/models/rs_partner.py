from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    dni = fields.Char(string="DNI")

    @api.constrains('dni')
    def _check_dni_required(self):
        for rec in self:
            # Exigir apenas se for cliente e houver eCommerce
            if rec.type in ['contact', 'private'] and not rec.dni:
                raise ValidationError("O campo DNI é obrigatório.")

