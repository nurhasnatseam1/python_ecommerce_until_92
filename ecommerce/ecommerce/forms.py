from django import forms


class ContactForm(forms.Form):
    fullname=forms.CharField()
    email=forms.EmailField()
    content=forms.CharField()



class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()
