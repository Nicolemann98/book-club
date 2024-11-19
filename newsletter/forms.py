from django import forms
from .models import NewsletterSubscription, Newsletter


class NewsletterSubscribeForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Ensure the email is not already subscribed
        if NewsletterSubscription.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already subscribed.")
        return email


class NewsletterUnsubscribeForm(forms.Form):
    email = forms.EmailField(label='Email Address', required=True)


class SendNewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = '__all__'
