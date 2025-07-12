{
    "name": "Hello Popup OWL",
    "version": "1.0",
    "category": "Website",
    "depends": ["website"],
    'assets': {
    'web.assets_frontend': [
        'hello_popup_owl/static/src/js/main.js',  # <-- CORRETO
        'hello_popup_owl/static/src/components/popup/popup_component.js',
        'hello_popup_owl/static/src/components/popup/popup_template.xml',
        'hello_popup_owl/static/src/css/popup.css',
    ],
},
    "installable": True,
    "application": False,
    'license': 'LGPL-3'
}


