{
    'name': "Obrigatoriedade do DNI no Checkout",
    'summary': "Adiciona e torna o campo DNI obrigatório para parceiros no checkout.",
    'version': '1.0',
    'category': 'Website/eCommerce',
    'depends': ['base', 'website_sale'], # 'website_sale' é necessário para a view do checkout
    'data': [
        'views/website_sale_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
}
