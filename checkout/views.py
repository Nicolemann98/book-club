from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
       'stripe_public_key': 'pk_test_51Q4QsfHvxENyFbwvvGe26GXRQltG7GiZ1ur2Dm2pewz2knvzcTQQlpPZsL4j7bSgHp0bf1qWa0V2Mx0bycPDsUvx004D3zKpIb',
       'client_secret': 'test client secret',
    }

    return render(request, template, context)