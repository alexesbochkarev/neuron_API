from django.urls import path

from . import views


app_name = 'tariffs'


urlpatterns = [

    path('payment_page', views.payment_page, name='payment_page'),
    path('success', views.success, name='success'),
    path('cancel', views.cancel, name='cancel'),
    path('stripe_webhoock', views.stripe_webhoock, name='stripe_webhoock'),

    path('payment_pack_300', views.payment_pack_300, name='payment_pack_300'),
    path('payment_pack_800', views.payment_pack_800, name='payment_pack_800'),
    path('payment_pack_2000', views.payment_pack_2000, name='payment_pack_2000'),
    path('payment_pack_5000', views.payment_pack_5000, name='payment_pack_5000'),
    path('payment_advanced', views.payment_advanced, name='payment_advanced')
]