from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.tools.translate import _


class PartnerDniCheckout(WebsiteSale):

    def _merge_name(self, values):
        """Combina first_name e last_name no campo name."""
        first_name = (values.get('first_name') or "").strip()
        last_name = (values.get('last_name') or "").strip()
        if first_name or last_name:
            values['name'] = (first_name + " " + last_name).strip()
        return values

    def address_form_validate(self, mode, all_values, data):
        """Valida dados do checkout (nome + DNI obrigatório)."""
        all_values = self._merge_name(all_values)

        errors, error_msgs = super().address_form_validate(mode, all_values, data)

        # Validação extra: DNI obrigatório
        dni = all_values.get('dni', '').strip()
        if not dni:
            errors['dni'] = 'missing'
            error_msgs.append(_("DNI é obrigatório."))

        return errors, error_msgs

    def address_form_save(self, partner_id, mode, all_values, data):
        """Salva dados do checkout garantindo nome completo."""
        all_values = self._merge_name(all_values)
        return super().address_form_save(partner_id, mode, all_values, data)

