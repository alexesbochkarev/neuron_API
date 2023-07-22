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


YOUR_DOMAIN = settings.YOUR_DOMAIN


@login_required(login_url='admin:login',)
def payment_page(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        # Retrieve the subscription & product
        tariff = Tariff.objects.get(user=request.user)
        return render(request, 'tariff/payment_page.html', {
            'tariff': tariff
        })

    except Tariff.DoesNotExist:
        return render(request, 'tariff/payment_page.html')
    return render(request, 'tariff/payment_page.html')

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


def payment(price: str, amount: int, mode: str, energy: int = None, request = None):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        if mode == 'payment':
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': price,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                customer_creation = 'always',
                success_url=YOUR_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=YOUR_DOMAIN + '/cancel',
                metadata={
                    'energy': energy,
                    'amount': amount,
                    }
            )
        if mode == 'subscription':
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': price,
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url=YOUR_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=YOUR_DOMAIN + '/cancel',
                metadata={
                    'amount': amount
                    }
                
            )
    except Exception as e:
        return str(e)
    return checkout_session


@login_required(login_url='admin:login',)
def payment_pack_300(request):
    if request.method == 'POST':
        session = payment(
            price='price_1NVbUlH7qCwTnShMP6wElWTS', 
            energy=300, 
            amount=9,
            mode='payment'
        )
    return redirect(session.url, code=303)

@login_required(login_url='admin:login',)
def payment_pack_800(request):
    if request.method == 'POST':
        session = payment(
            price='price_1NW0MqH7qCwTnShM72S4bYQL', 
            energy=800, 
            amount=19,
            mode='payment'
        )
    return redirect(session.url, code=303)
    

@login_required(login_url='admin:login',)
def payment_pack_2000(request):
    if request.method == 'POST':
        session = payment(
            price='price_1NW0uNH7qCwTnShMexjr7NKS', 
            energy=2000, 
            amount=39,
            mode='payment'
        )
    return redirect(session.url, code=303)
    

@login_required(login_url='admin:login',)
def payment_pack_5000(request):
    if request.method == 'POST':
        session = payment(
            price='price_1NW15fH7qCwTnShMYWvLHJw4', 
            energy=5000, 
            amount=79,
            mode='payment'
        )
    return redirect(session.url, code=303)
    

@login_required(login_url='admin:login',)
def payment_free(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        if user.tariff == None:
            tariff = Tariff.objects.get(name='Free')
            user.tariff = tariff
            user.energy = int(user.energy) + int(tariff.energy_copy)
            user.save()
            return redirect('/payment_page', code=303)
    return redirect('/payment_page', code=303)
            
    
@login_required(login_url='admin:login',)
def payment_advanced(request):
    if request.method == 'POST':
        session = payment(
            request=request,
            price='price_1NW31RH7qCwTnShMPj5T37vQ',
            amount=19,
            mode='subscription'
        )
    return redirect(session.url, code=303)


@login_required(login_url='admin:login',)
def payment_ultra(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        session = payment(
            request=request,
            price='price_1NWi6bH7qCwTnShMxvufMNjC',
            amount=39,
            mode='subscription'
        )
    return redirect(session.url, code=303)
    


@login_required(login_url='admin:login',)
def payment_proffesional(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        session = payment(
            request=request,
            price='price_1NWiBSH7qCwTnShMWF8iJDcy',
            amount=99,
            mode='subscription'
        )
    return redirect(session.url, code=303)


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
        user = User.objects.get(id=user_id)
        mode = event['data']['object']['mode']

        if mode == 'subscription':

            stripe_customer_id = session.get('customer')
            stripe_subscription_id = session.get('subscription')
            subscription = stripe.Subscription.retrieve(str(stripe_subscription_id))
            product = stripe.Product.retrieve(subscription.plan.product)
            tarif = Tariff.objects.create(
                name=str(product['metadata']['name']),
                energy_copy=int(product['metadata']['energy_copy']),
                refil=int(product['metadata']['refil']),
                price_month=int(product['metadata']['amount']),
                price_year=int(product['metadata']['price_year']),
                economie=int(product['metadata']['economy']),
                storage=float(product['metadata']['storage']),
                status=str(subscription['status']),
                stripeCustomerId=str(stripe_customer_id),
                stripeSubscriptionId=str(stripe_subscription_id),
            )

            user.tariff = tarif
            user.energy = int(user.energy) + int(product['metadata']['energy_copy'])
            user.save()

        else:

            energy = event['data']['object']['metadata']['energy']
            user.energy = int(user.energy) + int(energy)
            user.save()

        
    return HttpResponse(status=200)

