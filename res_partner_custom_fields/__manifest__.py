{
    'name': 'Dividir Nome e Adicionar DNI',
    'version': '1.0',
    'category': 'Contactos',
    'summary': 'Divide campo Full Name e adiciona campo DNI obrigatório',
    'depends': ['base', 'contacts'],
    'data': [
    'views/res_partner_views.xml',
    'views/website_sale_address_inherit.xml',
	],
    'installable': True,
    'auto_install': False,
}

