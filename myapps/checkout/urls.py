from django.conf.urls import *
from django.views.decorators.csrf import csrf_exempt

from . import views


urlpatterns = patterns('',
 
    url(r'place-order/$', views.SuccessResponseView.as_view(), name='sips-place-order'),
)