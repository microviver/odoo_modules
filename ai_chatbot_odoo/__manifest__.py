{
    'name': 'AI Chatbot Assistant',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Chatbot integrado com OpenAI Assistant',
    'depends': ['base', 'web', 'website'],
    'data': [
        'views/chatbot_template.xml',
    ],
    'assets': { 
        'web.assets_frontend': [
            'ai_chatbot_odoo/static/src/js/chatbot.js',
            'ai_chatbot_odoo/static/src/css/chatbot.css',
        ],
    },
    'installable': True,
}
