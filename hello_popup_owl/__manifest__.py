{
    'name': 'Hello Popup OWL',
    'version': '1.0.0',
    'depends': ['website'],
    'assets': {
    'web.assets_frontend': [
        'hello_popup_owl/static/src/components/popup/popup_template.xml',
        'hello_popup_owl/static/src/components/popup/popup_component.js',
        'hello_popup_owl/static/src/js/main.js',
        ],
    },
    'data': ['views/popup_snippet.xml'],
    'installable': True,
    'license': 'LGPL-3',
}
