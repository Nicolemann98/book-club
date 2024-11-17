from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import NewsletterSubscription
from .forms import NewsletterSubscriptionForm, NewsletterUnsubscriptionForm

def subscribe_newsletter(request):
    if request.method == "POST":
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'You have successfully subscribed to the newsletter!'
            )
            return redirect(reverse('home'))
        else:
            messages.error(
                request,
                'Failed to subscribe!'
            )
    else:
        form = NewsletterSubscriptionForm()

    return render(request, 'newsletter/subscribe.html', {'form': form})

def unsubscribe_newsletter(request):
    if request.method == "POST":
        form = NewsletterUnsubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                subscription = NewsletterSubscription.objects.get(email=email)
                subscription.delete()
                messages.success(request, f"Successfully unsubscribed {email}.")
                return redirect(reverse('home'))
            except NewsletterSubscription.DoesNotExist:
                messages.error(request, f"Email address {email} not found.")
        else:
            messages.error(
                request,
                'Failed to unsubscribe!'
            )
    else:
        form = NewsletterUnsubscriptionForm()

    return render(request, 'newsletter/unsubscribe.html', {'form': form})
