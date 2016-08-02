from oscar.app import Shop

from myapps.checkout.app import application as checkout_app
from myapps.partner.app import application as partner_app

class MyShop(Shop):
	checkout_app = checkout_app
	partner_app = partner_app

	print 'app.py'

application = MyShop()