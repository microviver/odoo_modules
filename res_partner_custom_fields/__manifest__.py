{
    'name': 'Partner Custom Fields',
    'version': '1.0.0',
    'category': 'Website/Website',
    'summary': 'Custom fields for res.partner model',
    'description': """
        This module adds custom fields to the res.partner model,
        including DNI field in the billing address form.
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['website_sale', 'base'],
    'data': [
        'views/res_partner_views.xml',
        'views/website_sale_templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
