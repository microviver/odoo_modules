{
    "name": "AI Chatbot Website",
    "version": "1.0",
    "category": "Website",
    "summary": "Chatbot com OpenAI integrado ao website",
    "depends": ["website"],
    "data": [
        "views/website_templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "ai_chatbot_website/static/src/js/chatbot.js",
        ],
    },
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}

