# __manifest__.py
{
    "name": "Hello Popup OWL",
    "version": "1.0",
    "summary": "Custom popup using OWL",
    "category": "Website",
    "depends": ["website"],
    "assets": {
        "web.assets_frontend": [
            # No 'main.js' anymore, as we use a direct trigger from popup_trigger_template.xml
            "hello_popup_owl/static/src/components/popup/popup_component.js",
            "hello_popup_owl/static/src/components/popup/popup_template.xml", # This is a QWeb template
            "hello_popup_owl/static/src/css/popup.css",
        ],
    },
    "data": [
        "views/popup_trigger_template.xml", # This file defines an Odoo view record
    ],
    "license": "LGPL-3",
}