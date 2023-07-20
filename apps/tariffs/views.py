from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

from .models import Payment, Tariff

import stripe
import time


User = get_user_model()


YOUR_DOMAIN = 'http://127.0.0.1:8000'


@login_required(login_url='admin:login',)
def payment_page(request):
    return render(request, 'tariff/payment_page.html')


@login_required(login_url='admin:login',)
def payment_pack_300(request):
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
                metadata={
                    'energy': 300,
                    'amount': 9,
                    'mode':'package'
                    }
            )
            print(checkout_session)
        except Exception as e:
            return str(e)

        return redirect(checkout_session.url, code=303)


@login_required(login_url='admin:login',)
def payment_pack_800(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': 'price_1NW0MqH7qCwTnShM72S4bYQL',
                        'quantity': 1,
                    },
                ],
                mode='payment',
                customer_creation = 'always',
                success_url=YOUR_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=YOUR_DOMAIN + '/cancel',
                metadata={
                    'energy': 800,
                    'amount': 19,
                    'mode':'package'
                    }
            )
            print(checkout_session)
        except Exception as e:
            return str(e)

        return redirect(checkout_session.url, code=303)
    

@login_required(login_url='admin:login',)
def payment_pack_2000(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': 'price_1NW0uNH7qCwTnShMexjr7NKS',
                        'quantity': 1,
                    },
                ],
                mode='payment',
                customer_creation = 'always',
                success_url=YOUR_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=YOUR_DOMAIN + '/cancel',
                metadata={
                    'energy': 2000,
                    'amount': 39,
                    'mode':'package'
                    }
            )
            print(checkout_session)
        except Exception as e:
            return str(e)

        return redirect(checkout_session.url, code=303)
    

@login_required(login_url='admin:login',)
def payment_pack_5000(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': 'price_1NW15fH7qCwTnShMYWvLHJw4',
                        'quantity': 1,
                    },
                ],
                mode='payment',
                customer_creation = 'always',
                success_url=YOUR_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=YOUR_DOMAIN + '/cancel',
                metadata={
                    'energy': 5000,
                    'amount': 79,
                    'mode':'package'
                    }
            )
            print(checkout_session)
        except Exception as e:
            return str(e)

        return redirect(checkout_session.url, code=303)
    

@login_required(login_url='admin:login',)
def payment_advanced(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': 'price_1NW31RH7qCwTnShMPj5T37vQ',
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url=YOUR_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=YOUR_DOMAIN + '/cancel',
                metadata={
                    'energy': 120,
                    'amount': 19,
                    'mode':'subscription',
                    'tariff': 'Advanced'
                    }
            )
        except Exception as e:
            return str(e)

        return redirect(checkout_session.url, code=303)
    


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
        session = event['data']['object']
        session_id = session.get('id', None)
        time.sleep(15)
        amount = event['data']['object']['metadata']['amount']
        # Payment update
        user_payment = Payment.objects.get(session_id=session_id)
        user_payment.amount = int(amount)
        user_payment.status = True
        user_payment.save()
        # User update
        user_id = user_payment.user.id
        energy = event['data']['object']['metadata']['energy']
        mode = event['data']['object']['metadata']['mode']
        user = User.objects.get(id=user_id)
        if mode == 'subscription':
            tariff_name = event['data']['object']['metadata']['tariff']
            tarif = Tariff.objects.get(name=tariff_name)
            user.tariff = tarif
            user.energy = int(user.energy) + int(energy)
            user.save()
        else:
            user.energy = int(user.energy) + int(energy)
            user.save()
        
    return HttpResponse(status=200)
