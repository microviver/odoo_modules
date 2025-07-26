{
    "name": "Homepage Popup Discount",
    "version": "1.0",
    "author": "Wadiana",
    "category": "Website",
    "depends": ["website_sale", "mass_mailing"],
      'data': [
	    'data/mail_template.xml',
	    'views/homepage_popup.xml',
	    'views/popup_discount_views.xml'
	],
    'assets': {
        'web.assets_frontend': [
            'popup_discount/static/src/js/popup_discount_notification.js',
            'popup_discount/static/src/css/popup_discount_notification.css',
        ],
    },
    "installable": True,
    "application": False,
}
