{
    "name": "my_hello_popup",
    "version": "1.0",
    "summary": "Exibe um alerta Hello no frontend do website",
    "author": "Wadiana",
    "license": "LGPL-3",
    "depends": ["base", "web", "website"],
    "assets": {
        "web.assets_frontend": [
            "my_hello_popup/static/src/js/hello_popup.js",
        ],
    },
    "data": [],
    "installable": True,
    "application": False,
    "test_disable": True
}
