from oscar.apps.checkout.views import PaymentDetailsView as OscarPaymentDetailsView
from oscar.apps.payment import models
from oscar.apps.payment.forms import BankcardForm

from myapps.sips.facade import Facade


class PaymentDetailsView(OscarPaymentDetailsView):
    '''
    Deze PaymentDetailsView overschrijft de default django-oscar implementatie, dewelke niets doet.
    Het is verantwoordelijk voor het communiceren met de payment facade en de betaling te initieren.
    De submit() methode 
    De handle_payment() methode update django-oscar met de nodige gegevens na betaling
    '''

    print '-----------tim PaymentDetailsView----------'


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

        print '********' + 'handle_payment' + '*************'
        print 'order nummer: ' + str(order_number) + ' -- bedrag: ' + str(total.incl_tax)

        for (key, value) in kwargs:
            print key + ': ' + value

        print '++ einde ++'

        facade = Facade()

        print 'facade aangemaakt?'

        payment_ref = facade.pre_authorise(order_number, total.incl_tax)

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

    def submit(self, user, basket, shipping_address, shipping_method, shipping_charge, billing_address, order_total, payment_kwargs=None, order_kwargs=None):
        '''
        Deze methode dient blijkbaar niet overschreven te worden en wordt opgeroepen vooraleer handle_payment() wordt opgeroepen
        '''

        print '))))))) submit() methode (((((((('
        print basket

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

        print '^^^^^^^^^ handle_payment_details_submission ^^^^^^^^^'

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