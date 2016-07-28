import requests
import httplib
import logging

from django import http
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlencode
from django.utils.decorators import method_decorator

from oscar.apps.checkout.views import PaymentDetailsView as OscarPaymentDetailsView
from oscar.apps.checkout.views import OrderPlacementMixin
from oscar.apps.checkout.views import ThankYouView as OscarThankYouView
from oscar.apps.payment import models
from oscar.apps.payment.forms import BankcardForm
from oscar.apps.payment.exceptions import RedirectRequired, PaymentError, UnableToTakePayment
from oscar.apps.order.utils import OrderNumberGenerator

from braces.views import JsonRequestResponseMixin

from myapps.sips.facade import Facade


logger = logging.getLogger('oscar.checkout')

class SipsRedirectRequired(RedirectRequired):
    '''
    Custom subklasse van Oscar's RedirectRequired, waarbij we enkele bijkomende argumenten toevoegen
    '''

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

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentDetailsView, self).dispatch(request, *args, **kwargs)

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

        print 'checkout view: handle_payment methode'

        facade = Facade()

        url, redirectionVersion, redirectionData = facade.pre_authorise(order_number, total.incl_tax)

        source_type, __ = models.SourceType.objects.get_or_create(
                    name="Sips")
        source = models.Source(
            source_type=source_type,
            amount_allocated=total.incl_tax,
            reference=reference)
            #reference=order_number)
        self.add_payment_source(source)

        # Record payment event
        self.add_payment_event('auth', total.incl_tax)



        # Gateway initiates payment with Sips Connector  which returns url + submit data

        '''try:
            url, redirectionVersion, redirectionData = facade.pre_authorise(order_number, total.incl_tax)

            raise SipsRedirectRequired(url, redirectionVersion, redirectionData)

        except UnableToTakePayment as e:
            # Er heeft zich een fout voorgedaan bij SIPS authorisatie

            print 'unable to take payment'

            msg = e
            logger.warning("Order #%s: unable to take payment (%s) - restoring basket",order_number, msg)
            self.restore_frozen_basket()

            messages.error(self.request, ("We were unable to authorise your order: %s") % e)

            url = reverse('dashboard:order-detail', kwargs={'number': order_number})
            response = http.HttpResponseRedirect(url)

            return response'''


            #return self.render_payment_details(self.request, error=msg)

            #print 'error' + str(e)
            #raise SipsRedirectRequired('/', None, None)


        '''data = {
            'redirectionVersion': redirectionVersion,
            'redirectionData': redirectionData
        }'''

        #logger.info("Order: redirecting to %s", url)

        #print 'data' + str(data)

        # 
        #raise SipsRedirectRequired(url, redirectionVersion, redirectionData)


        #print 'we gaan verder na redirect required!!!'

        # Payment successful! Record payment source
        '''source_type, __ = models.SourceType.objects.get_or_create(
            name="SomeGateway")
        source = models.Source(
            source_type=source_type,
            amount_allocated=total.incl_tax,
            reference=reference)
        self.add_payment_source(source)

        # Record payment event
        self.add_payment_event('auth', total.incl_tax)'''



    def submiiit(self, user, basket, shipping_address, shipping_method, shipping_charge, billing_address, order_total, payment_kwargs=None, order_kwargs=None):
        '''
        Deze methode roept handle_payment() op, en verwerkt eventuele fouten die handle_payment() retourneert
        '''

        print 'checkout view: submit methode'

        # generator is responsible for generating basket id, this will be used for order processing
        generator = OrderNumberGenerator()
        order_number = generator.order_number(basket)


        try:
            # roep handle_payment() op
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


        return super(PaymentDetailsView, self).submit(user,basket,shipping_address,shipping_method,shipping_charge,billing_address,order_total,payment_kwargs,order_kwargs)



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

        # No form data to validate by default, so we simply render the preview
        # page.  If validating form data and it's invalid, then call the
        # render_payment_details view.
        return self.render_preview(request)


    def post(self, request, *args, **kwargs):

        return super(PaymentDetailsView, self).post(request, *args, **kwargs)

class SuccessResponseView(JsonRequestResponseMixin, OscarPaymentDetailsView):

    print 'success response view - checkout.views'

    template_name_preview = 'sips/preview.html'

    def get(self, request, *args, **kwargs):

        print '---------RETURN GET ---------'

        return None

    def post(self, request, *args, **kwargs):

        print ' ++++++ success response view: POST methode'

        try: 
            data = request.POST['data']
            print data

        except KeyError:

            print 'shiiiiiiiiiiiiiiiiiit!'

class ThankYouView(JsonRequestResponseMixin, OscarThankYouView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):

        print 'mythankyouview'

        return super(ThankYouView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        print 'post'

        total = 1000
        reference = 'reference'

        # Payment successful! Record payment source
        source_type, __ = models.SourceType.objects.get_or_create(
            name="SomeGateway")
        source = models.Source(
            source_type=source_type,
            amount_allocated=total,
            reference=reference)
        self.add_payment_source(source)

        # Record payment event
        self.add_payment_event('auth', total)

        return super(ThankYouView, self).get(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        print 'get'

        print args
        print kwargs
        print request.GET

        return super(ThankYouView, self).get(self, request, *args, **kwargs)


