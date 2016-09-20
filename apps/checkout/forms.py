from django import forms
from django.utils.translation import ugettext_lazy as _
from oscar.apps.checkout.forms import GatewayForm as CoreGatewayForm


class GatewayForm(CoreGatewayForm):
    username = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'My email address is', 'class':'form-control'}))
    GUEST, NEW, EXISTING = 'anonymous', 'new', 'existing'
    CHOICES = (
        (GUEST, _('I am a new customer and want to checkout as a guest')),
        (NEW, _('I am a new customer and want to create an account '
                'before checking out')),
        (EXISTING, _('I am a returning customer, and my password is')))
    options = forms.ChoiceField(widget=forms.widgets.RadioSelect,
                                choices=CHOICES, initial=GUEST)