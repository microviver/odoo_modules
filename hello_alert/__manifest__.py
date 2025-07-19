{
    'name': 'my_homepage_module',

    'version': '1.0',
    'depends': ['website'],
    'assets': {
        'web.assets_frontend': [
            'my_homepage_module/static/src/components/homepage_alert.js',
            'my_homepage_module/static/src/components/homepage_alert.xml',
            'my_homepage_module/static/src/js/main.js',
        ],
    },
    'installable': True,
}

