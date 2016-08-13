from django.views.generic import TemplateView, View

from custom.models import CustomImage, ThumbnailImage


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

		thumbnails = ThumbnailImage.objects.all()

		context = {}
		context['image_list'] = thumbnails

		return context

class VisitUsView(TemplateView):
	'''
	'''
	template_name = 'visit-us.html'



