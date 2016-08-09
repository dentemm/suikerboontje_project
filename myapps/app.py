from oscar.app import Shop

from myapps.checkout.app import application as checkout_app
from myapps.partner.app import application as partner_app
from myapps.dashboard.app import application as dashboard_app

class MyShop(Shop):
	checkout_app = checkout_app
	partner_app = partner_app
	dashboard_app = dashboard_app

	print 'app.py'

application = MyShop()