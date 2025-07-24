{
    'name': 'Homepage Popup Captura Email',
    'version': '1.0',
    'summary': 'Popup na homepage para captura de email com desconto e subscrição da newsletter',
    'description': 'Este módulo adiciona um popup na página inicial que recolhe o email do visitante, envia um código de desconto e subscreve à newsletter.',
    'category': 'Website',
    'author': 'Marco & Copilot 😎',
    'depends': ['website', 'mail'],
    'data': [
        'views/homepage_popup.xml',
        'data/mail_template.xml',
    ],
    'installable': True,
    'application': False,
}

