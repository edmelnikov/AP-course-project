from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64)
    password = forms.CharField(label='Password', max_length=64, widget=forms.PasswordInput)


class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64)
    email = forms.EmailField(label='Email', max_length=128)
    password = forms.CharField(label='Password', max_length=64, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Confirm your password', max_length=64, widget=forms.PasswordInput)




