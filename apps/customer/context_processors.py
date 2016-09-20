from oscar.apps.customer.forms import PasswordResetForm
from apps.customer.forms import EmailAuthenticationForm

def forms_processor(request):
    return {
        'login_form': EmailAuthenticationForm(request.get_host()),
        'password_reset_form': PasswordResetForm()
    }
