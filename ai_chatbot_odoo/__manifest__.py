{
    "name": "AI Chatbot Odoo",
    "version": "1.0",
    "category": "Website",
    "summary": "Chatbot com OpenAI integrado ao website",
    "author": "Espírito Digital",
    "license": "LGPL-3",
    "depends": ["website"],
    "assets": {
        "web.assets_frontend": [
            "ai_chatbot_odoo/static/src/js/chatbot_toggle.js",
            "ai_chatbot_odoo/static/src/css/chatbot.css",
            "ai_chatbot_odoo/static/src/js/chatbot.js"
        ],
    },
    "data": [
        "views/chatbot_template.xml",
    ],
    "installable": True,
    "application": False,
}

