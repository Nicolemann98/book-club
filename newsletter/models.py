from django.db import models


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)


class Newsletter(models.Model):
    date_sent = models.DateTimeField(auto_now_add=True)
    subject = models.TextField(blank=True, default="")
    body = models.TextField(blank=True, default="")


class NewsletterSent(models.Model):
    newsletter = models.ForeignKey(
        Newsletter,
        on_delete=models.CASCADE
    )
    email = models.EmailField(unique=False)