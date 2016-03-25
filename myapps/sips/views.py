from django.views.generic import RedirectView

class SipsRedirectView(RedirectView):
	'''
	Dit view is verantwoordelijk voor de redirect naar de Sips Paypage nadat
	de Sips Connector het initialization request heeft goedgekeurd
	'''
	

	def get_redirect_url(self, **kwargs):

		pass
