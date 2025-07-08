{
    "name": "my_hello_popup",
    "version": "1.0",
    "summary": "Show hello popup on backend",
    "author": "Wadiana",
    "license": "LGPL-3",
    "depends": ["web"],  # só precisa do 'web' para backend
    "assets": {
        "web.assets_backend": [
            "my_hello_popup/static/src/js/hello_popup.js",
        ]
    },
    "installable": True,
    "application": False,
    "test_disable": True
}
