{
    "name": "Hello Popup OWL",
    "version": "1.0",
    "summary": "Custom popup using OWL",
    "category": "Website",
    "depends": ["web", "website"],
    "assets": {
        "web.assets_frontend": [
            "hello_popup_owl/static/src/js/main.js",
            "hello_popup_owl/static/src/components/popup/popup_component.js",
            "hello_popup_owl/static/src/css/popup.css"
        ]
    },
    "data": [
        "static/src/components/popup/popup_template.xml"
    ],
    "license": "LGPL-3",
}