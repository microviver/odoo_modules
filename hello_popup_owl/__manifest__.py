{
    "name": "Hello Popup OWL",
    "version": "1.0",
    "summary": "Custom popup using OWL",
    "category": "Website",
    "depends": ["website"],
    "assets": {
        "web.assets_frontend": [
            # "hello_popup_owl/static/src/js/main.js", # Remove this
            "hello_popup_owl/static/src/components/popup/popup_template.xml",
            "hello_popup_owl/static/src/components/popup/popup_component.js",
            "hello_popup_owl/static/src/js/popup_service.js", # Add this
            "hello_popup_owl/static/src/css/popup.css",
        ],
    },
    # ...
    "data": [
        "views/popup_view.xml",
    ],
    # ...
    "license": "LGPL-3",
}