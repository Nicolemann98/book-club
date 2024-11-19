from django.contrib import admin
from .models import NewsletterSubscription, Newsletter, NewsletterSent

# Register your models here.


class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'date_subscribed',
    )


class NewsletterAdmin(admin.ModelAdmin):
    list_display = (
        'date_sent',
    )


class NewsletterSentAdmin(admin.ModelAdmin):
    list_display = (
        'newsletter',
        'email',
    )


admin.site.register(NewsletterSubscription, NewsletterSubscriptionAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(NewsletterSent, NewsletterSentAdmin)
