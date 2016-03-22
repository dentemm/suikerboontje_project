from oscar.app import Shop

from myapps.checkout.app import application as checkout_app

class MyShop(Shop):
	checkout_app = checkout_app

	print 'app.py'

application = MyShop()