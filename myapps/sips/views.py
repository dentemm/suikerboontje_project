from django.views.generic import RedirectView, View

from oscar.apps.checkout.views import OrderPlacementMixin, PaymentDetailsView

from braces.views import JsonRequestResponseMixin


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


class SuccessResponseView(JsonRequestResponseMixin, PaymentDetailsView):
	'''
	Handle response from Sips
	'''

	print '--------success response view --------------'

	template_name_preview = 'sips/sips.html'

	def post(self, request, *args, **kwargs):

		print ' ------------------ RETURN POST -------------'

		print 'return data: ' + str(request.POST.get('Data', 'default'))

		return super(SuccessResponseView, self).post(request, *args, **kwargs)

	def get(self, request, *args, **kwargs):

		print '---------RETURN GET ---------'

		return None
	

class ConfirmView(OrderPlacementMixin, View):
    """
    Handle the response from GoCardless
    """

    template_name = 'test.html'

    def get(self, request, *args, **kwargs):

        print '--------- RETURN get ------------'

        try:
            facade.confirm(request)
        except PaymentError, e:
            messages.error(self.request, str(e))
            self.restore_frozen_basket()
            return HttpResponseRedirect(reverse('checkout:payment-details'))

        # Fetch submission data out of session
        order_number = self.checkout_session.get_order_number()
        basket = self.get_submitted_basket()
        total_incl_tax, total_excl_tax = self.get_order_totals(basket)

        # Record payment source
        source_type, is_created = SourceType.objects.get_or_create(name='GoCardless')
        source = Source(source_type=source_type,
                        currency='GBP',
                        amount_allocated=total_incl_tax,
                        amount_debited=total_incl_tax)
        self.add_payment_source(source)

        # Place order
        return self.handle_order_placement(order_number,
                                           basket,
                                           total_incl_tax,
                                           total_excl_tax)

	def post(self, request, *args, **kwargs):

		print '--------- RETURN post------------'

		try:
		    facade.confirm(request)
		except PaymentError, e:
		    messages.error(self.request, str(e))
		    self.restore_frozen_basket()
		    return HttpResponseRedirect(reverse('checkout:payment-details'))

		# Fetch submission data out of session
		order_number = self.checkout_session.get_order_number()
		basket = self.get_submitted_basket()
		total_incl_tax, total_excl_tax = self.get_order_totals(basket)

		# Record payment source
		source_type, is_created = SourceType.objects.get_or_create(name='GoCardless')
		source = Source(source_type=source_type,
		                currency='GBP',
		                amount_allocated=total_incl_tax,
		                amount_debited=total_incl_tax)
		self.add_payment_source(source)

		# Place order
		return self.handle_order_placement(order_number,
		                                   basket,
		                                   total_incl_tax,
		                                   total_excl_tax)




