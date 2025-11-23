from odoo import fields, models

class ResPartner(models.Model):
    # Herdamos o modelo de Contatos/Parceiros
    _inherit = 'res.partner'

    dni = fields.Char(
        string='DNI',
        required=True, # Torna o campo obrigatório no modelo
        help='Documento Nacional de Identidad ou Número de Identificación Fiscal.'
    )
