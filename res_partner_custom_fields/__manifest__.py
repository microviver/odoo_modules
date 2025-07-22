# __manifest__.py
{
    'name': 'Website Sale DNI Field',
    'version': '1.0',
    'depends': ['website_sale'],
    'data': [
        'views/shop_address_inherit.xml',
        'views/res_partner_form_inherit.xml',  # <--- adiciona aqui!
    ],
}

