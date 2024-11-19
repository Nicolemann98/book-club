from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import (NewsletterSubscription,
    NewsletterSent,
    Newsletter
)
from .forms import (
    NewsletterSubscribeForm,
    NewsletterUnsubscribeForm,
    SendNewsletterForm
)

def subscribe_newsletter(request):
    if request.method == "POST":
        form = NewsletterSubscribeForm(request.POST)
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
        form = NewsletterSubscribeForm()

    return render(request, 'newsletter/subscribe.html', {'form': form})

def unsubscribe_newsletter(request):
    if request.method == "POST":
        form = NewsletterUnsubscribeForm(request.POST)
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
        form = NewsletterUnsubscribeForm()

    return render(request, 'newsletter/unsubscribe.html', {'form': form})

@login_required
def send_newsletter(request):
    def send_emails(newsletter):
        all_subscriptions = NewsletterSubscription.objects.all()
        email_addresses = []
        for subscription in all_subscriptions:
            email_addresses.append(subscription.email)
            newsletter_sent = NewsletterSent(newsletter=newsletter, email=subscription.email)
            newsletter_sent.save()

        send_mail(
            newsletter.subject,
            newsletter.body,
            settings.DEFAULT_FROM_EMAIL,
            email_addresses,
            fail_silently=False
        )
        
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        form = SendNewsletterForm(request.POST)
        if form.is_valid():
            try:
                newsletter = form.save()
                send_emails(newsletter)
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
        form = SendNewsletterForm()
    
    return render(request, 'newsletter/manage.html', {'form': form})

def view_newsletters(request):
    newsletters = Newsletter.objects.all().order_by('date_sent')

    if request.user.is_superuser:
        newsletter_recipients = {}
        for newsletter in newsletters:
            recipients_query = NewsletterSent.objects.all().filter(newsletter=newsletter)
            recipients_email = []
            for recipient in recipients_query:
                recipients_email.append(recipient.email)
            newsletter_recipients[newsletter] = recipients_email
        return render(
            request,
            'newsletter/newsletter_list.html',
            {'newsletter_recipients': newsletter_recipients}
        )


    return render(
        request,
        'newsletter/newsletter_list.html',
        {'newsletters': newsletters}
    )
