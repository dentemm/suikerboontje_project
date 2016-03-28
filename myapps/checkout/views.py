import requests
import httplib
import logging

from django import http
from django.utils.http import urlencode

from oscar.apps.checkout.views import PaymentDetailsView as OscarPaymentDetailsView
from oscar.apps.checkout.views import OrderPlacementMixin
from oscar.apps.payment import models
from oscar.apps.payment.forms import BankcardForm
from oscar.apps.payment.exceptions import RedirectRequired, PaymentError
from oscar.apps.order.utils import OrderNumberGenerator


from myapps.sips.facade import Facade


logger = logging.getLogger('oscar.checkout')

class SipsRedirectRequired(RedirectRequired):

    def __init__(self, url, version, data):

        self.url = url
        self.redirectionVersion = version
        self.redirectionData = data


class PaymentDetailsView(OscarPaymentDetailsView):
    '''
    Deze PaymentDetailsView overschrijft de default django-oscar implementatie, dewelke niets doet.
    Het is verantwoordelijk voor het communiceren met de payment facade en de betaling te initieren.
    De submit() methode 
    De handle_payment() methode update django-oscar met de nodige gegevens na betaling
    '''

    def get_context_data(self, **kwargs):
        '''
        Het bankkaart form dient toegevoegd te worden aan de context
        EDIT: niet nodig voor BCMC
        '''
        # Add bankcard form to the template context
        ctx = super(PaymentDetailsView, self).get_context_data(**kwargs)
        #ctx['bankcard_form'] = kwargs.get('bankcard_form', BankcardForm())
        
        return ctx

    def handle_payment(self, order_number, total, **kwargs):
        '''
        Deze methode is verantwoordelijk voor payment processing 
        ''' 

        facade = Facade()

        # Gateway initiates payment with Sips Connector  which returns url + submit data
        url, redirectionVersion, redirectionData = facade.pre_authorise(order_number, total.incl_tax)

        data = {
            'redirectionVersion': redirectionVersion,
            'redirectionData': redirectionData
        }

        logger.info("Order: redirecting to %s", url)

        # 
        raise SipsRedirectRequired(url, redirectionVersion, redirectionData)


    

        # Payment successful! Record payment source
        source_type, __ = models.SourceType.objects.get_or_create(
            name="SomeGateway")
        source = models.Source(
            source_type=source_type,
            amount_allocated=total.incl_tax,
            reference=reference)
        self.add_payment_source(source)

        # Record payment event
        self.add_payment_event('auth', total.incl_tax)


        raise RedirectRequired(url)

    def submit(self, user, basket, shipping_address, shipping_method, shipping_charge, billing_address, order_total, payment_kwargs=None, order_kwargs=None):
        '''
        Deze methode roept handle_payment() op, en verwerkt eventuele fouten die handle_payment() retourneert
        '''

        # generator is responsible for generating basket id, this will be used for order processing
        generator = OrderNumberGenerator()
        order_number = generator.order_number(basket)


        try:
            self.handle_payment(order_number, order_total, **payment_kwargs)

        except SipsRedirectRequired as e:

            logger.info("Order #%s: redirecting to %s", order_number, e.url)

            data = {
                'redirectionVersion': e.redirectionVersion,
                'redirectionData': e.redirectionData
            }

            # urlencode retourneert url parameters
            payload = urlencode(data)

            # volledige url bestaat uit base url + urlencoded parameters
            complete_url = '%s?%s' % (e.url, payload)


            return http.HttpResponseRedirect(complete_url)


        return super(PaymentDetailsView, self).submit(user,basket, shipping_address, shipping_method,shipping_charge,billing_address,order_total,payment_kwargs,order_kwargs)



    def handle_payment_details_submission(self, request):
        '''
        Deze methode wordt opgeroepen wanneer je in de checkout procedure naar de 'preview' stap gaat
        Hij is vereist wanneer de gebruiker een bijkomend form (vb bankkaart formulier) dient in te vullen
        De methode leidt de gebruiker verder naar het preview view wanneer de submitted data correct is
        Wanneer de data incorrect is wordt het view opnieuw gerenderd met de nodige foutmeldingen
        '''

        '''
        In dit geval is het form dat we nodig hebben het BankcardForm uit de payment app
        '''


        #bankcard_form = BankcardForm(request.POST)

        # Check bankcard form is valid
        '''if bankcard_form.is_valid():

            return self.render_preview(
                    request, bankcard_form=bankcard_form
                )

        # Form invalid: re-render
        return self.render_payment_details(request, bankcard_form=bankcard_form)'''


        # No form data to validate by default, so we simply render the preview
        # page.  If validating form data and it's invalid, then call the
        # render_payment_details view.
        return self.render_preview(request)


    def post(self, request, *args, **kwargs):

        print '-------zou het ?????? ---------'

        return super(PaymentDetailsView, self).post(request, *args, **kwargs)

class SuccessResponseMixin(OscarPaymentDetailsView):

    template_name_preview = 'sips/preview.html'


    def post(self, request, *args, **kwargs):

        try: 
            data = request.POST['data']
            print data

        except KeyError:

            print 'shiiiiiiiiiiiiiiiiiit!'

