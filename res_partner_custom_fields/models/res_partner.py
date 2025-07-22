from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    dni = fields.Char(
        string='DNI',
        help='Document Number (DNI, CPF, etc.)',
        size=20,
        copy=False
    )
    
    @api.constrains('dni')
    def _check_dni_unique(self):
        """Optional: Make DNI unique per company"""
        for record in self:
            if record.dni:
                existing = self.search([
                    ('dni', '=', record.dni),
                    ('id', '!=', record.id),
                    ('company_id', '=', record.company_id.id or self.env.company.id)
                ])
                if existing:
                    raise ValidationError('DNI must be unique!')
