from django.views.generic import TemplateView, View

from custom.models import CustomImage


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

		images = CustomImage.objects.all()



		'''myrange = range(1,31)

		urls = []

		for i in myrange:

			if i < 10:
				url = 'img0' + str(i) +'.jpg'

			else:
				url = 'img' + str(i) +'.jpg'


			urls.append(url)'''

		context = {}



		context['images'] = images

		return context

class VisitUsView(TemplateView):
	'''
	'''
	template_name = 'visit-us.html'



