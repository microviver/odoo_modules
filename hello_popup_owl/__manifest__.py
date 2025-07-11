{
    "name": "Hello Popup OWL",
    "summary": "Popup simples OWL com mensagem 'Hello!'",
    "version": "1.0.0",
    "author": "wadiana",
    "license": "LGPL-3",
    "category": "Website",
    "depends": ["website"],
    "assets": {
        "web.assets_frontend": [
            "hello_popup_owl/static/src/components/popup/popup_component.js",
            "hello_popup_owl/static/src/components/popup/popup_template.xml",
            "hello_popup_owl/static/src/js/main.js",
            "hello_popup_owl/static/src/css/popup.css",
        ],
    },
    "data": ["views/popup_snippet.xml"],
    "installable": True,
    "application": False,
}
