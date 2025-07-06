from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    firstname = fields.Char('Nombre', required=False)
    lastname = fields.Char('Apellidos', required=False)
    dni = fields.Char('DNI', required=False)

    @api.model
    def create(self, vals):
        vals = self._compose_name(vals)
        return super().create(vals)

    def write(self, vals):
        vals = self._compose_name(vals)
        return super().write(vals)

    def _compose_name(self, vals):
        firstname = vals.get('firstname') or self.firstname
        lastname = vals.get('lastname') or self.lastname
        if firstname and lastname:
            vals['name'] = f"{firstname} {lastname}"
        return vals
