from odoo import models, fields, api

class PopupDiscountCode(models.Model):
    _name = 'popup.discount.code'
    _description = 'Popup Discount Code'
    _order = 'create_date desc' # Ordena por data de criação

    name = fields.Char(string='Código de Desconto', compute='_compute_name', store=True) # Nome para exibição
    email = fields.Char(string='E-mail do Cliente', required=True, help="E-mail do cliente que recebeu o código de desconto.")
    code = fields.Char(string='Código', required=True, readonly=True, copy=False, help="Código de desconto único.")
    used = fields.Boolean(string='Usado', default=False, help="Indica se o código de desconto já foi utilizado.")
    create_date = fields.Datetime(string='Data de Geração', readonly=True, default=fields.Datetime.now, help="Data e hora em que o código foi gerado.")
    used_date = fields.Datetime(string='Data de Uso', help="Data e hora em que o código foi utilizado.")
    sale_order_id = fields.Many2one('sale.order', string='Ordem de Venda', help="Ordem de venda onde o código de desconto foi aplicado.")

    # Para garantir que o email seja único (um email, um código de desconto)
    _sql_constraints = [
        ('code_unique', 'unique(code)', 'O código de desconto deve ser único!'),
        ('email_unique', 'unique(email)', 'Este e-mail já recebeu um código de desconto!'),
    ]

    @api.depends('code')
    def _compute_name(self):
        for record in self:
            record.name = f"Código de Desconto: {record.code}"
