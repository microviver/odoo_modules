{
    "name": "website_discount_popup",
    "version": "1.0",
    "summary": "Show popup asking email in exchange for 5% discount",
    "author": "Wadiana",
    "license": "LGPL-3",
    'depends': ['base', 'web', 'website'],
    "assets": {
        "web.assets_frontend": [
            "web/static/src/legacy/js/public/public_widget.js",
            "web/static/lib/owl/owl.js",  # OWL core, necessário para componentes OWL
            "web/static/src/core/utils/functions.js",
            "website/static/src/js/website.utils.js",
            # Os teus ficheiros customizados:
            "website_discount_popup/static/src/js/popup.js",
            "website_discount_popup/static/src/css/popup.css",
        ],
    },
    "data": [
        "views/discount_popup_template.xml"
    ],
    "installable": True,
    "application": False,
    "test_disable": True
}
