from django.shortcuts import render,redirect
from .forms import ContactForm,LoginForm


def home_page(request):
    context={
        'title':'hello you are in the home page',
    }
    return render(request,'home_page.html',context)

def about_page(request):
    context={
        'title':'hello you are in the about page',
    }
    return render(request,'home_page.html',context)

def contact_page(request):
    context={
        'title':'hello you are in the contact page',
        'form':ContactForm
    }
    if request.method=='POST':
        context['title']=request.POST.get('fullname')
    return render(request,'contact/view.html',context)


def login_page(request):
    form=LoginForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
    context={}

    return render(request,'auth/login.html',context)

def register_page(request):
    form=LoginForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
    context={}
    return render(request,'auth/register.html',context)
