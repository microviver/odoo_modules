{
    "name": "Homepage Popup Discount",
    "version": "1.0",
    "author": "Wadiana",
    "category": "Website",
    "depends": ["website_sale", "mass_mailing"],
      "data": [
        "views/popup_discount_views.xml",
        "views/homepage_popup.xml",
        "data/mail_template.xml", # Certifique-se que esta linha está presente
    ],
    "installable": True,
    "application": False,
}
