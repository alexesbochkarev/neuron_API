from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Payment

import stripe
import time



YOUR_DOMAIN = 'http://127.0.0.1:8000'


@login_required(login_url='admin:login',)
def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': 'price_1NVbUlH7qCwTnShMP6wElWTS',
                        'quantity': 1,
                    },
                ],
                mode='payment',
                customer_creation = 'always',
                success_url=YOUR_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=YOUR_DOMAIN + '/cancel',
                metadata={'energy': 300}
            )
            print(checkout_session)
        except Exception as e:
            return str(e)

        return redirect(checkout_session.url, code=303)
    
    return render(request, 'tariff/checkout.html')


def success(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    user_id = request.user
    # user_payment = Payment.objects.get(user=user_id)
    Payment.objects.create(
        user=user_id,
        session_id=checkout_session_id,
        amount=9,
        method='Stripe'
        )
    return render(request, 'tariff/success.html', {'customer': customer})


def cancel(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return render(request, 'tariff/cancel.html')

@csrf_exempt
def stripe_webhoock(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    time.sleep(10)
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        print(event['data']['object']['metadata']['energy'])
        session = event['data']['object']
        session_id = session.get('id', None)
        time.sleep(15)
        user_payment = Payment.objects.get(session_id=session_id)
        user_payment.status = True
        user_payment.save()
        
    return HttpResponse(status=200)
