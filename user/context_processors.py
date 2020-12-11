from .forms import CreateAccountForm
from django.contrib.auth.forms import AuthenticationForm

def add_auth_forms(request):
	return {
		'login_form': AuthenticationForm(),
		'create_account_form':CreateAccountForm(),
	}