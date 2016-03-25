from django.conf.urls import *
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = patterns('',

	url(r'^redirect/', views.SipsRedirectView.as_view(), name='sips-redirect'),

)