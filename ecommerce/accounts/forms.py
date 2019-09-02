from django import forms
from django.contrib.auth import get_user_model





User=get_user_model()
class GuestLoginForm(forms.Form):
    email=forms.EmailField(label='email')

class LoginForm(forms.Form):
    username    =   forms.CharField()
    password    =   forms.CharField(widget=forms.PasswordInput)



class RegisterForm(forms.Form):
    username    =   forms.CharField(label='username')
    email       =   forms.EmailField(label='email')
    password    =   forms.CharField(label='password',widget=forms.PasswordInput)
    password_2  =   forms.CharField(label='Confirm password',widget=forms.PasswordInput)


    def clean_username(self):
        username=self.cleaned_data.get('username')
        qs=User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError('Username is token')
        return username
    def clean_email(self):
        email=self.cleaned_data.get('email')
        qs=User.objects.filter(email=email)
        if qs.exists():
            raise ValidationError('email is token')

        return email
    def clean(self):
        password=self.cleaned_data.get('password')
        password_2=self.cleaned_data.get('password_2')
        if password != password_2:
            raise forms.ValidationError('passwords do not match')
