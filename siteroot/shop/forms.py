from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Ваш юзернейм', max_length=64)
    password = forms.CharField(label='Ваш пароль', max_length=64, widget=forms.PasswordInput)


class SignupForm(forms.Form):
    username = forms.CharField(label='Ваш ник', max_length=64)
    email = forms.EmailField(label='Ваша почта', max_length=128)
    password = forms.CharField(label='Ваш пароль', max_length=64, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Подтвердите пароль', max_length=64, widget=forms.PasswordInput)




