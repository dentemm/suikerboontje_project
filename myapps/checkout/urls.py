'''from django.conf.urls import *
from django.views.decorators.csrf import csrf_exempt

from . import views


urlpatterns = patterns('',
 
    url(r'place-order/$', views.SuccessResponseView.as_view(), name='sips-place-order'),
)'''

'''from oscar.app import application

urlpatterns = [
    # Your other URLs
    url(r'thank-you/$', self.thankyou_view.as_view(), name='thank-you')

    url(r'', include(application.urls)),
]'''