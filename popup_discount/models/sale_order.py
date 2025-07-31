from odoo import models, api, fields
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Adicionar um campo para armazenar o código de desconto aplicado
    applied_discount_code_id = fields.Many2one(
        'popup.discount.code', 
        string='Código de Desconto Aplicado', 
        readonly=True, 
        help="Código de desconto do popup utilizado nesta ordem de venda."
    )

    def _apply_popup_discount(self, code):
        """
        Aplica o desconto de 5% à ordem de venda usando o código fornecido.
        """
        # (Your existing _apply_popup_discount method remains the same)
        discount_code_record = self.env['popup.discount.code'].sudo().search([
            ('code', '=', code),
            ('used', '=', False)
        ], limit=1)

        if discount_code_record:
            if self.applied_discount_code_id:
                raise UserError("Um código de desconto já foi aplicado a esta ordem.")

            if discount_code_record.sale_order_id and discount_code_record.sale_order_id != self:
                raise UserError("Este código de desconto já foi usado em outra ordem.")

            discount_amount = self.amount_total * 0.05
            
            discount_product = self.env['product.product'].sudo().search([('name', '=', 'Desconto Popup 5%')], limit=1)
            if not discount_product:
                discount_product = self.env['product.product'].sudo().create({
                    'name': 'Desconto Popup 5%',
                    'type': 'service',
                    'list_price': 0,
                    'default_code': 'DISCOUNT_POPUP_5',
                    'invoice_policy': 'order',
                    'purchase_ok': False,
                    'sale_ok': True,
                    'detailed_type': 'service',
                })
                _logger.info("Produto 'Desconto Popup 5%' criado automaticamente.")

            self.write({
                'order_line': [(0, 0, {
                    'product_id': discount_product.id,
                    'product_uom_qty': 1,
                    'price_unit': -discount_amount,
                    'name': f"Desconto de 5% (código: {code})",
                })]
            })

            discount_code_record.write({
                'used': True,
                'used_date': fields.Datetime.now(),
                'sale_order_id': self.id,
            })
            self.applied_discount_code_id = discount_code_record.id

            _logger.info(f"Código de desconto {code} aplicado com sucesso na Ordem de Venda {self.name}.")
            return True
        else:
            _logger.warning(f"Tentativa de usar código de desconto inválido ou já usado: {code}")
            return False

    # Sobrescrever o método 'write' para capturar atualizações no `client_order_ref`
    def write(self, vals):
        res = super().write(vals)
        if 'client_order_ref' in vals and self.state == 'draft':
            code = vals.get('client_order_ref')
            if code:
                self._apply_popup_discount(code)
        return res

    # Sobrescrever o método create para capturar o código na criação da ordem
    @api.model
    def create(self, vals_list): # Changed parameter name to vals_list
        # vals_list will be a list of dictionaries, even if only one record is being created
        orders = super().create(vals_list)
        
        # Iterate over the created orders and apply the discount
        for order in orders:
            code = order.client_order_ref # Access client_order_ref directly from the created order record
            if code:
                try:
                    order._apply_popup_discount(code)
                except UserError as e:
                    _logger.warning(f"Failed to apply discount for order {order.name}: {e.name}")
                    # You might want to handle this error more gracefully,
                    # e.g., by logging it and continuing, or raising the error
                    # depending on your business logic. For now, it will just log.
        return orders
