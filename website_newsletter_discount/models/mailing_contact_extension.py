from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class MassMailingContact(models.Model):
    _inherit = 'mass.mailing.contact'

    @api.model_create_multi
    def create(self, vals_list):
        contacts = super().create(vals_list)
        for contact in contacts:
            if contact.email:
                self._send_welcome_discount_email(contact)
        return contacts

    def _send_welcome_discount_email(self, contact):
        coupon_program = self.env.ref('website_newsletter_discount.newsletter_welcome_discount_program', raise_if_not_found=False)

        if not coupon_program:
            raise UserError(_("Discount program 'Newsletter Welcome Discount' not found. Please create it first."))

        coupon_code = self.env['ir.sequence'].next_by_code('sale.coupon.code')
        if not coupon_code:
            raise UserError(_("Sequence for coupon codes not found. Please define 'sale.coupon.code' sequence."))

        coupon = self.env['sale.coupon'].create({
            'program_id': coupon_program.id,
            'code': coupon_code,
            'expiration_date': fields.Date.add(fields.Date.today(), months=1),
        })

        partner = self.env['res.partner'].search([('email', '=', contact.email)], limit=1)
        if not partner:
            partner = self.env['res.partner'].create({
                'name': contact.name or contact.email,
                'email': contact.email,
                'is_company': False,
                'type': 'contact',
            })
        coupon.partner_id = partner.id

        template = self.env.ref('website_newsletter_discount.email_template_welcome_discount', raise_if_not_found=False)
        if template:
            try:
                template.with_context(coupon_code=coupon.code, contact_name=contact.name or contact.email).send_mail(contact.id, force_send=True)
                self.env.cr.commit()
            except Exception as e:
                _logger.error("Failed to send welcome discount email to %s: %s", contact.email, e)
        else:
            raise UserError(_("Email template 'Welcome Discount Email' not found. Please ensure it's loaded."))
