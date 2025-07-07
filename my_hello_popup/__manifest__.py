# -*- coding: utf-8 -*-
{
    'name': "My Hello Popup",
    'summary': "Um módulo Odoo simples para exibir um popup 'Hello !' em JavaScript.",
    'description': """
        Este módulo demonstra como incluir JavaScript customizado no Odoo 18
        para exibir um popup de alerta simples.
    """,
    'author': "Seu Nome/Empresa",
    'website': "http://www.seusite.com",
    'category': 'Technical',
    'version': '18.0.1.0.0',
    'depends': ['web'],
    'data': [
        'views/assets.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}