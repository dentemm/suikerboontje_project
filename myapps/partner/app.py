from oscar.apps.partner import app

from myapps.partner import views


class PartnerApplication(app.PartnerApplication):
    pass


application = CheckoutApplication()