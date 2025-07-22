from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    nombre = fields.Char(string="Nombre", required=True)
    apellido = fields.Char(string="Apellido", required=True)
    dni = fields.Char(string="DNI", required=True)
    
    name = fields.Char(compute="_compute_name", store=True)

    @api.depends('nombre', 'apellido')
    def _compute_name(self):
        for partner in self:
            partner.name = f"{partner.nombre or ''} {partner.apellido or ''}".strip()

    @api.constrains('dni')
    def _validate_dni(self):
        for partner in self:
            dni = partner.dni
            if not dni or len(dni) != 9 or not dni[:-1].isdigit() or not dni[-1].isalpha():
                raise ValidationError("DNI inválido: deve ter 8 dígitos seguidos de uma letra.")
            numero = int(dni[:-1])
            letra = dni[-1].upper()
            letras_validas = "TRWAGMYFPDXBNJZSQVHLCKE"
            letra_calculada = letras_validas[numero % 23]
            if letra != letra_calculada:
                raise ValidationError(f"DNI inválido: letra '{letra}' não corresponde ao número. Letra correta seria '{letra_calculada}'.")

