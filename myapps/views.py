from django.views.generic import TemplateView, View


#from braces.views import JsonRequestResponseMixin


# Load views dynamically
#PaymentDetailsView = get_class('checkout.views', 'PaymentDetailsView')
#CheckoutSessionMixin = get_class('checkout.session', 'CheckoutSessionMixin')	

class InfoView(TemplateView):
	'''
	'''
	template_name = 'wat-doen-we.html'


class PresentationView(TemplateView):
	'''
	'''
	template_name = 'presentaties.html'

class VisitUsView(TemplateView):
	'''
	'''
	template_name = 'visit-us.html'

