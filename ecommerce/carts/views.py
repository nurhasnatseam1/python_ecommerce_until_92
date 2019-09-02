from django.shortcuts import render,redirect
from .models import Cart
from products.models import Product
from orders.models import Order
from accounts.forms import LoginForm,GuestLoginForm
from accounts.models import GuestEmail
from billing.models import BillingProfile
from address.forms import AddressForm
from address.models import Address
# Create your views here.

def cart_create(user=None):##you will initialize the cart here
    cart_obj=Cart.objects.create(user=user)
    return cart_obj

def cart_home(request):
    cart_obj,new_obj=Cart.objects.new_or_get(request)
    return render(request,'carts/home.html',{'object':cart_obj})



def cart_update(request): #you will send request here to add or remove a product from cart
    product_id=request.POST.get('product_id')
    try:
      obj=Product.objects.get(id=product_id)
    except Product.DoesNotExist:
      print('show message to user, product is gone')
      return redirect('carts:cart_home')
    cart_obj,new_obj=Cart.objects.new_or_get(request)
    if product_obj in cart_obj.products.all():
        cart_obj.product.remove(obj)
    else:
        cart_obj.products.add(obj)
    return redirect(product_obj.get_absolute_url())


def checkout_home(request): ##this is where you see the ordering
    cart_obj,cart_created=Cart.objects.new_or_get(request)
    if cart_created or cart_obj.products.count()==0:
        return redirect('carts:cart_home')
    user=request.user
#    billing_profile=None
#    guest_email_id=request.session.get('guest_email_id')
#    if user.is_authenticated:
#        #logged in user checkot
#        billing_profile,billing_profile_created=BillingProfile.objects.get_or_create(user=user,email=user.email)
#    elif guest_email_id is not None:
#        #guest user checkout
#        guest_email_obj=GuestEmail.objects.get(id=guest_email_id)
#        billing_profile,billing_guest_profile_created=BillingProfile.objects.get_or_create(email=guest_email_obj.email)
    billing_address_id=request.session.get('billing_address_id',None)
    shipping_address_id=request.session.get('shipping_address_id',None)
    billing_profile,billing_profile_created=BillingProfile.objects.get_or_new(request)
    order_obj=None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs=Address.objects.filter(billing_profile=billing_profile)
#        order_qs=Order.objects.filter(cart=cart_obj,billing_profile=billing_profile,active=True)
#        if order_qs.exists() and order_qs.count()==1:
#            order_obj=order_qs.first()
#        else:
            #old_order_qs=Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj,active=True)
            #if old_order_qs.exists():
            #    old_order_qs.update(active=False)
        order_obj,order_obj_created=Order.objects.get_or_new(cart_obj=cart_obj,billing_profile=billing_profile)
        if shipping_address_id:
            order_obj.shipping_address=Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address=Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if billing_address_id or shipping_address_id:
            order_obj.save()


    if request.method=='POST':
        #check the order is done
        is_done=order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            del request.session['cart_id']
            return redirect('/cart/success/')

    context={
        'object':order_obj,
        'billing_profile':billing_profile,
        'login_form':LoginForm(),
        'guest_login_form':GuestLoginForm(),
        'shipping_address_form':AddressForm(),
        'billing_address_form':AddressForm(),
        'address_qs':address_qs
    }
    return render(request,'carts/checkout.html',context)
