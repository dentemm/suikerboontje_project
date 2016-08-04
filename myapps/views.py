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

	def get_context_data(self, **kwargs):

		myrange = range(1,31)

		urls = []

		for i in myrange:

			if i < 10:
				url = 'oscar/presentaties/img0' + str(i) +'.jpg'

			else:
				url = 'oscar/presentaties/img' + str(i) +'.jpg'


			urls.append(url)


		context = {}

		context['urls'] = urls

		return context

class VisitUsView(TemplateView):
	'''
	'''
	template_name = 'visit-us.html'



