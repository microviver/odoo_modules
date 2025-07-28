from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    first_name = fields.Char("Nombre")
    last_name = fields.Char("Apellidos")
    dni = fields.Char("DNI")

