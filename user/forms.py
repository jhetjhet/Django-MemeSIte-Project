from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class CreateAccountForm(UserCreationForm):
	email = forms.EmailField(label='Email')

	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password1',
			'password2'
		]

class ProfileForm(forms.Form):
	email = forms.EmailField(required=False)
	first_name = forms.CharField(required=False)
	last_name = forms.CharField(required=False)
	profile_picture = forms.ImageField(required=False)
	background = forms.ImageField(required=False)

	def __init__(self, *args, **kwargs):
		try:
			self.uid = kwargs.pop('uid')
			super().__init__(*args, **kwargs)
		except KeyError:
			raise forms.ValidationError('profile form required uid value')
		except User.DoesNotExist:
			raise forms.ValidationError(f'user with uid {self.uid} does not exist')

	def save(self, *args, **kwargs):
		cleaned_data = self.cleaned_data
		user = User.objects.get(pk=self.uid)
		user.email = cleaned_data.get('email')
		user.first_name = cleaned_data.get('first_name')
		user.last_name = cleaned_data.get('last_name')

		profile_picture = cleaned_data.get('profile_picture')
		if profile_picture:
			user.profile.picture = profile_picture

		background = cleaned_data.get('background')
		if background:
			user.background = background
			
		user.save()
		user.profile.save()
		return user