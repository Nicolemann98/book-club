from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import NewsletterSubscription, NewsletterSent
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
    def send_email(newsletter):
        all_subscriptions = NewsletterSubscription.objects.all()
        for subscription in all_subscriptions:
            # TODO send email
            newsletter_sent = NewsletterSent(newsletter=newsletter, newsletter_subscription=subscription)
            newsletter_sent.save()
        
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        form = NewsletterManagementForm(request.POST)
        if form.is_valid():
            try:
                newsletter = form.save()
                send_email(newsletter)
                messages.success(request, 'Successfully sent newsletter!')
                return redirect(reverse('home'))
            except Exception as e:
                print("ERROR!")
                print(e)
                messages.error(
                    request,
                    "Failed to send newsletter."
                )
        else:
            messages.error(
                request,
                'Failed to send newsletter. Please ensure the form is valid.'
            )
    else:
        form = NewsletterManagementForm()
    
    return render(request, 'newsletter/manage.html', {'form': form})
