{
    'name': 'Hello Popup OWL',
    'version': '1.0.0',
    'depends': ['website'],
    'assets': {
        'web.assets_frontend': [
            'hello_popup_owl/static/src/components/popup_template.xml',
            'hello_popup_owl/static/src/js/main.js',
            'hello_popup_owl/static/src/components/popup_component.js'
        ],
    },
    'data': ['views/popup_snippet.xml'],
    'installable': True,
}
