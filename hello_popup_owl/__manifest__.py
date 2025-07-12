{
    "name": "Hello Popup OWL",
    "version": "1.0",
    "summary": "Custom popup using OWL",
    "category": "Website",
    "depends": ["website"],
    "assets": {
        "web.assets_frontend": [
            "hello_popup_owl/static/src/components/popup/popup_component.js",
            "hello_popup_owl/static/src/components/popup/popup_template.xml", # This is a QWeb template
            "hello_popup_owl/static/src/css/popup.css",
            "hello_popup_owl/static/src/js/popup_main.js", # <--- ADD THIS LINE
        ],
    },
    "data": [
        # popup_trigger_template.xml is only needed if it defines an Odoo view record,
        # e.g., for creating a page. If its only purpose was to inject the script,
        # you might not need it anymore. If it's a website template for some other
        # purpose (e.g., a dynamic block), keep it.
        # If its sole purpose was the <script> tag, you can probably remove it
        # from 'data' and delete the file.
        # Let's assume for now it defines a view, so keep it for now but remove the script inside.
        "static/views/popup_trigger_template.xml",
    ],
    "license": "LGPL-3",
}