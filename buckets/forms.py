from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import IntegrityError

class LoginSignupForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    action = forms.CharField(widget=forms.HiddenInput)

    def clean(self):
        action = self.cleaned_data.get('action')
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if self.errors:
            return self.cleaned_data

        if action == 'Signup':
            try:
                User.objects.create_user(username, '', password)
            except IntegrityError, e:
                raise forms.ValidationError("Username already taken.")

        if authenticate(username=username, password=password) is None:
            raise forms.ValidationError("Invalid username or password.")

        return self.cleaned_data