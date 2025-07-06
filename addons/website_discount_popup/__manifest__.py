{
    "name": "Website Discount Popup",
    "version": "1.0",
    "summary": "Popup for email capture and discount offer",
    "author": "Wadiana",
    "license": "LGPL-3",
    "depends": ["website"],
    "data": [
        "views/discount_popup_template.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_discount_popup/static/src/js/popup.js",
            "website_discount_popup/static/src/css/popup.css",
        ],
    },
    "installable": True,
    "application": False,
}
