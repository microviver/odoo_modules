{
    "name": "ai_chatbot_odoo",
    "version": "1.0",
    "summary": "Chatbot with AI for website",
    "author": "Wadiana",
    "license": "LGPL-3",
    "depends": ["base", "web", "website"],
    "assets": {
        "website.assets_frontend": [
            "ai_chatbot_odoo/static/src/js/chatbot.js",
            "ai_chatbot_odoo/static/src/css/chatbot.css"
        ]
    },
    "installable": True,
    "application": False
}
