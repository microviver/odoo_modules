{
    'name': "Website Newsletter Discount",
    'summary': "Adds a newsletter subscription box to a website page and sends a discount coupon.",
    'version': '1.0',
    'category': 'Website/eCommerce',
    'author': "Marco",
    'license': 'LGPL-3',
    'depends': [
        'website',
        'mass_mailing',
        'sale_coupon',
        'sale_management',
    ],
    'data': [
        'data/ir_sequence_data.xml',
        'data/email_template.xml',
        'views/website_templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}