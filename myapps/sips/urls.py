'''from django.conf.urls import *
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = patterns('',

	url(r'^redirect/', views.SipsRedirectView.as_view(), name='sips-redirect'),

)
'''
from django.conf.urls import *
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from . import views


urlpatterns = patterns('',
    #url(r'^redirect/', views.RedirectView.as_view(), name='gocardless-redirect'),
    url(r'^confirm/$', csrf_exempt(views.ConfirmView.as_view()), name='sips-response'),
    url(r'^place-order/$', csrf_exempt(views.SuccessResponseView.as_view()), name='sips-place-order'),
    #url(r'^cancel/', views.CancelView.as_view(), name='gocardless-cancel'),
)