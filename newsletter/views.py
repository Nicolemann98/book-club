from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewsletterSubscriptionForm

def subscribe_newsletter(request):
    if request.method == "POST":
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully subscribed to the newsletter!')
            return redirect(reverse('home'))
    else:
        form = NewsletterSubscriptionForm()

    return render(request, 'newsletter/subscribe.html', {'form': form})