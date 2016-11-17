from django.conf.urls import url
from . import views

urlpatterns = [
    #order
	url(r'^orderPage/$', views.orderPage, name='orderPage'),
	url(r'^CheckoutInfo/$', views.CheckoutInfo, name='CheckoutInfo'),
	url(r'^ask/$',views.ask2Login,name='ask'),
	url(r'^guestOrderHistory/$', views.guestOrderHistory, name='guestOrderHistory'),
	url(r'^orderRequest/$', views.OrderRequest, name='orderRequest'),
	url(r'^changeDuration/$', views.changeDuration, name = 'changeDuration'),

]