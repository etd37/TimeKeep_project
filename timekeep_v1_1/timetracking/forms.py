from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


# Create your forms here.
from .models import UserProfile


class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		profile = UserProfile(user=user)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
			profile.save()
		return user


class EditProfileForm(UserChangeForm):
	password = None

	class Meta:
		model = User
		fields = ("first_name", "last_name", "email")

