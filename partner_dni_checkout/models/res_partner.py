from odoo import fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"

    first_name = fields.Char(string="Nome")
    last_name = fields.Char(string="Apelido")
    dni = fields.Char(string="DNI/NIF")

    def _compute_display_name(self):
        for partner in self:
            if partner.first_name or partner.last_name:
                partner.display_name = f"{partner.first_name or ''} {partner.last_name or ''}".strip()
            else:
                partner.display_name = partner.name or ''

