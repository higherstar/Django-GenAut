from django.shortcuts import redirect
from oscar.apps.customer.views import AccountRegistrationView as CoreAccountRegistrationView, \
    AccountAuthView as CoreAccountAuthView
from .forms import EmailUserCreationForm, UserAddressForm
from django.views import generic
from django.conf import settings
from django.contrib.auth import logout as auth_logout

from django.http import *
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


class AccountAuthView(CoreAccountAuthView):
    login_prefix = ''


class AccountRegistrationView(CoreAccountRegistrationView):
    def get_context_data(self, *args, **kwargs):
        ctx = super(AccountRegistrationView, self).get_context_data(*args, **kwargs)
        if not 'address_form' in kwargs.keys():
            ctx['address_form'] = UserAddressForm()
        return ctx

    def forms_invalid(self, user_form, address_form):
        return self.render_to_response(self.get_context_data(form=user_form, address_form=address_form))

    def post(self, *args, **kwargs):
        user_form = EmailUserCreationForm(host=None, data=self.request.POST)
        address_form = UserAddressForm(self.request.POST)
        user_form_valid = user_form.is_valid()
        address_form_valid = address_form.is_valid()
        if user_form_valid and address_form_valid:
            #user = self.register_user(user_form)
            user = user_form.save(commit=False)
            user.first_name = address_form.cleaned_data['first_name']
            user.last_name = address_form.cleaned_data['last_name']
            user.title = address_form.cleaned_data['title']
            user.save()
            address = address_form.save(commit=False)
            address.user = user
            address.save()
            return redirect(user_form.cleaned_data['redirect_url'])
        else:
            return self.forms_invalid(user_form, address_form)

class LogoutView(generic.RedirectView):
    url = settings.OSCAR_HOMEPAGE
    permanent = False

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        response = super(LogoutView, self).get(request, *args, **kwargs)

        for cookie in settings.OSCAR_COOKIES_DELETE_ON_LOGOUT:
            response.delete_cookie(cookie)

        return response


def login_user(request):
    #logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
    return render_to_response('custom_login.html', context_instance=RequestContext(request))
