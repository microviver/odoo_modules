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
    "license": "LGPL-3",
}