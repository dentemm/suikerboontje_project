from django.views.generic import RedirectView

# Load views dynamically
#PaymentDetailsView = get_class('checkout.views', 'PaymentDetailsView')
#CheckoutSessionMixin = get_class('checkout.session', 'CheckoutSessionMixin')	

class SipsRedirectView(RedirectView):
	'''
	Dit view is verantwoordelijk voor de redirect naar de Sips Paypage nadat
	de Sips Connector het initialization request heeft goedgekeurd
	'''
	

	def get_redirect_url(self, **kwargs):

		pass

'''
class SuccessResponseView(PaymentDetailsView):

	template_name_preview = 'sips/preview.html'
	'''




