from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import re


class ResPartner(models.Model):
    _inherit = 'res.partner'

    firstname = fields.Char(string='First Name') # Removed required=True
    lastname = fields.Char(string='Last Name')   # Removed required=True
    dni = fields.Char(string='DNI / NIF / CPF', size=20, copy=False) # Removed required=True
    
    @api.constrains('dni')
    def _check_dni_nif_nie(self):
        for partner in self:
            if partner.dni:
                dni_value = partner.dni.upper()
                dni_pattern = r'^\d{8}[A-Z]$'
                nie_pattern = r'^[XYZ]\d{7}[A-Z]$'

                if re.match(dni_pattern, dni_value):
                    if not self._validate_spanish_id_checksum(dni_value):
                        raise ValidationError(_("Invalid DNI/NIF checksum for %s. Please check the number and letter.", dni_value))
                elif re.match(nie_pattern, dni_value):
                    if not self._validate_spanish_id_checksum(dni_value):
                        raise ValidationError(_("Invalid NIE checksum for %s. Please check the number and letter.", dni_value))
                else:
                    raise ValidationError(_("Invalid DNI format for %s. It should be 8 digits + 1 letter.", dni_value))

    def _validate_spanish_id_checksum(self, id_number):
        letters = "TRWAGMYFPDXBNJZSQVHLCKE"
        id_number = id_number.upper()

        if id_number[0].isalpha():  # NIE
            if id_number[0] == 'X':
                numeric_part = '0' + id_number[1:-1]
            elif id_number[0] == 'Y':
                numeric_part = '1' + id_number[1:-1]
            elif id_number[0] == 'Z':
                numeric_part = '2' + id_number[1:-1]
            else:
                return False
        else:  # DNI/NIF
            numeric_part = id_number[:-1]

        try:
            checksum_index = int(numeric_part) % 23
            return letters[checksum_index] == id_number[-1]
        except ValueError:
            return False
