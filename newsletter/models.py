from django.db import models


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)


class Newsletter(models.Model):
    date_sent = models.DateTimeField(auto_now_add=True)
    # file storage location


class NewsletterSent(models.Model):
    newsletter = models.ForeignKey(
        Newsletter,
        on_delete=models.CASCADE
    )
    newsletter_subscription = models.ForeignKey(
        NewsletterSubscription,
        on_delete=models.CASCADE
    )