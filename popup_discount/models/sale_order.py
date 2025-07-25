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
        discount_code_record = self.env['popup.discount.code'].sudo().search([
            ('code', '=', code),
            ('used', '=', False)
        ], limit=1)

        if discount_code_record:
            # Verifica se já aplicamos um código de desconto nesta ordem
            if self.applied_discount_code_id:
                raise UserError("Um código de desconto já foi aplicado a esta ordem.")

            # Verifica se o código de desconto já está associado a outra ordem
            # Embora 'used=False' já impeça, é uma checagem extra
            if discount_code_record.sale_order_id and discount_code_record.sale_order_id != self:
                raise UserError("Este código de desconto já foi usado em outra ordem.")


            # Calcular o valor do desconto
            discount_amount = self.amount_total * 0.05
            
            # Criar ou encontrar um produto para o desconto
            # É recomendável ter um produto específico para "Desconto" no Odoo.
            # Se não existir, pode criar um programaticamente ou pedir para criar manualmente.
            discount_product = self.env['product.product'].sudo().search([('name', '=', 'Desconto Popup 5%')], limit=1)
            if not discount_product:
                # Cria um produto de serviço para representar o desconto
                discount_product = self.env['product.product'].sudo().create({
                    'name': 'Desconto Popup 5%',
                    'type': 'service',
                    'list_price': 0, # Preço base 0
                    'default_code': 'DISCOUNT_POPUP_5',
                    'invoice_policy': 'order',
                    'purchase_ok': False,
                    'sale_ok': True,
                    'detailed_type': 'service', # Para Odoo 15+
                })
                _logger.info("Produto 'Desconto Popup 5%' criado automaticamente.")

            # Adicionar uma linha de ordem de venda para o desconto
            # O preço unitário será negativo
            self.write({
                'order_line': [(0, 0, {
                    'product_id': discount_product.id,
                    'product_uom_qty': 1,
                    'price_unit': -discount_amount, # Aplica o desconto como um valor negativo
                    'name': f"Desconto de 5% (código: {code})",
                })]
            })

            # Marcar o código como usado e associá-lo à ordem de venda
            discount_code_record.write({
                'used': True,
                'used_date': fields.Datetime.now(),
                'sale_order_id': self.id,
            })
            self.applied_discount_code_id = discount_code_record.id # Guarda a referência na SO

            _logger.info(f"Código de desconto {code} aplicado com sucesso na Ordem de Venda {self.name}.")
            return True
        else:
            _logger.warning(f"Tentativa de usar código de desconto inválido ou já usado: {code}")
            return False

    # Sobrescrever o método 'write' para capturar atualizações no `client_order_ref`
    def write(self, vals):
        res = super().write(vals)
        if 'client_order_ref' in vals and self.state == 'draft': # Apenas se for rascunho
            code = vals.get('client_order_ref')
            if code:
                # Remove o desconto existente se o código for alterado para um novo
                # Esta parte foi comentada na explicação anterior por razões de "uso único"
                # Mas aqui está a implementação caso precise:
                # if self.applied_discount_code_id and self.applied_discount_code_id.code != code:
                #    self._remove_existing_discount() 
                
                # Tenta aplicar o novo desconto
                self._apply_popup_discount(code)
        return res

    # Sobrescrever o método create para capturar o código na criação da ordem
    @api.model
    def create(self, vals):
        order = super().create(vals)
        code = vals.get('client_order_ref')
        if code:
            order._apply_popup_discount(code)
        return order
    
    # Esta função _remove_existing_discount() não é estritamente necessária para o requisito de "uso único"
    # Pois um código, uma vez aplicado e validado, é considerado usado.
    # Mas se a ordem for desfeita antes da confirmação final, e o código precisar ser reutilizado,
    # uma lógica mais complexa seria necessária. Por enquanto, mantemos o conceito de "usado" = consumido.
    # def _remove_existing_discount(self):
    #     if self.applied_discount_code_id:
    #         discount_line = self.order_line.filtered(lambda l: l.product_id.default_code == 'DISCOUNT_POPUP_5' and l.price_unit < 0)
    #         if discount_line:
    #             discount_line.unlink()
    #         self.applied_discount_code_id = False
