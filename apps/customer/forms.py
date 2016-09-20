from django import forms
from django.utils.translation import ugettext_lazy as _
from oscar.apps.customer.forms import EmailAuthenticationForm as CoreEmailAuthenticationForm,\
                                      EmailUserCreationForm as CoreEmailUserCreationForm
from oscar.core.loading import get_model
from oscar.core.validators import password_validators


class EmailAuthenticationForm(CoreEmailAuthenticationForm):
    username = forms.EmailField(label=_('Email address'),
                                widget=forms.EmailInput(attrs={'class': 'form-control',
                                                               'placeholder': 'example@mail.com', }))
    password = forms.CharField(label=_('Password'),
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Password', }),
                               validators=password_validators)
    redirect_url = forms.CharField(widget=forms.HiddenInput, required=False)


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = get_model('address', 'useraddress')
        exclude = (
            'user',
            'search_text',
            'is_default_for_shipping',
            'is_default_for_billing',
            'num_orders',
        )


class EmailUserCreationForm(CoreEmailUserCreationForm):
    email = forms.EmailField(label=_('Email address'),
                             widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': 'example@mail.com', }))
    password1 = forms.CharField(label=_('Password'),
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Password', }),
                                validators=password_validators)
    password2 = forms.CharField(label=_('Confirm password'),
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Confirm Password', }))
    redirect_url = forms.CharField(widget=forms.HiddenInput, required=False)
