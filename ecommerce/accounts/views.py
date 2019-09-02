from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,get_user_model
from django.http import HttpResponse
from django.utils.http import is_safe_url
from .models import GuestEmail
from .forms import LoginForm,RegisterForm,GuestLoginForm
# Create your views here.


def guestLoginView(request):
    form=GuestLoginForm(request.POST or None)
    context={
        'form':form
    }
    next_=request.GET.get('next')
    next_post=request.POST.get('next')
    redirect_path= next_ or next_post or None
    print('%%%%%%%%%%%%%%% %%%%%%%%%%% ')
    print(redirect_path)
    if form.is_valid():
        email=form.cleaned_data.get('email')
        new_guest_email=GuestEmail.objects.create(email=email)
        request.session['guest_email_id']=new_guest_email.id
        if is_safe_url(redirect_path,request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('/')
    return redirect('/register/')


def loginView(request):
    form=LoginForm(request.POST or None)
    context={
        'form':form
    }
    next_=request.GET.get('next')
    next_post=request.POST.get('next') or None
    redirect_path= next_ or next_post
    if form.is_valid():
        username    =   form.cleaned_data.get('username')
        password    =   form.cleaned_data.get('password')
        user        =   authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            try:
                del request.session['guest_email_id']  ### when we login i want to del the guest_billing_profile that is why i del the session variable
                ##and there will be a billing_profile automatically created for that user
            except:
                pass
            if is_safe_url(redirect_path,request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')
    return render(request,'accounts/login.html',context)



User=get_user_model()
def registerView(request):
    form=RegisterForm(request.POST or None)
    context={
    'form' :form
    }
    next_=request.GET.get('next')
    next_post=request.POST.get('next')
    redirect_path=next_ or next_post
    if form.is_valid():
        username=form.cleaned_data.get('username')
        email=form.cleaned_data.get('email')
        password=form.cleaned_data.get('password')
        new_user=User.objects.create(email=email,username=username,password=password)
        if new_user is not None:
            if is_safe_url(redirect_path,request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')
    return render(request,'accounts/register.html',context)
