{
    "name": "ai_chatbot_odoo",
    "version": "1.0",
    "summary": "Chatbot with AI for website",
    "author": "Wadiana",
    "license": "LGPL-3",
    "depends": ["base", "web", "website"],
    "assets": {
        "web.assets_frontend": [
            "web/static/lib/owl/owl.js",
            "web/static/src/core/utils/functions.js",
            "web/static/src/public/widget/public_widget.js",  # necessário para o import funcionar
            "ai_chatbot_odoo/static/src/js/chatbot.js",
            "ai_chatbot_odoo/static/src/css/chatbot.css"
        ]
    },
    "data": [
        "views/chatbot_template.xml"
    ],
    "installable": True,
    "application": False,
    "test_disable": True,
}

