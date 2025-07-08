{
    "name": "ai_chatbot_odoo",
    "version": "1.0",
    "summary": "Chatbot with AI for website",
    "author": "Wadiana",
    "license": "LGPL-3",
    "depends": ["base", "web", "website"],
    "assets": {
    "web.assets_frontend": [
        "web/static/src/js/public/public_widget.js",
        "web/static/lib/owl/owl.js",
        "web/static/src/core/utils/functions.js",
        "website/static/src/js/website.utils.js",
        "ai_chatbot_odoo/static/src/js/chatbot.js",
        "ai_chatbot_odoo/static/src/css/chatbot.css"
        ]
    },
    "installable": True,
    "application": False,
    "test_disable": True,
}

