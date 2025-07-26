{
    "name": "Homepage Popup Discount",
    "version": "1.0",
    "author": "Wadiana",
    "category": "Website",
    "depends": ["website_sale", "mass_mailing"],
      'data': [
	    'models/discount_code.py',  # This line is critical
	    'models/sale_order.py',
	    'data/mail_template.xml',
	    'views/*.xml',
	],
    "installable": True,
    "application": False,
}
