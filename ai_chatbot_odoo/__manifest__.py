{
    'name': 'AI Chatbot Assistant',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Chatbot integrado com OpenAI Assistant',
    'depends': ['base', 'web'],
    'assets': {
    'web.assets_frontend': [
        'ai_chatbot_odoo/static/src/js/main.js',
        'ai_chatbot_odoo/static/src/components/chatbot/chatbot_template.xml',
        'ai_chatbot_odoo/static/src/styles/chatbot.scss',
    ],
    },    
    'installable': True,
}