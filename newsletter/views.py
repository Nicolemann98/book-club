from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import NewsletterSubscription
from .forms import (
    NewsletterSubscriptionForm,
    NewsletterUnsubscriptionForm,
    NewsletterManagementForm
)

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

@login_required
def manage_newsletter(request):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        form = NewsletterManagementForm(request.POST)
        if form.is_valid():
            # send emails, add all to NewsletterSent model
            newsletter = form.save()
            messages.success(request, 'Successfully sent newsletter!')
            return redirect(reverse('home'))
        else:
            messages.error(
                request,
                'Failed to send newsletter. Please ensure the form is valid.'
            )
    else:
        form = NewsletterManagementForm()
    
    return render(request, 'newsletter/manage.html', {'form': form})