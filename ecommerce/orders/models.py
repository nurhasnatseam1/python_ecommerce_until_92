from django.db import models
from carts.models import Cart
import string
from django.db.models.signals import pre_save,post_save
import random
from billing.models import BillingProfile
from address.models import Address
# Create your models here.

ORDER_STATUS_CHOICES=(
    ('created','Created'),
    ('paid','Paid'),
    ('shipping','Shipping'),
    ('refunded','Refunded'),
)
def random_string_generator(size=10,chars=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size) )


def unique_order_id_generator(instance,new_slug=None):
    order_id=random_string_generator()
    klass=instance.__class__

    qs_exists=klass.objects.filter(order_id=order_id).exists()
    if qs_exists:
        new_order_id=f"{order_id}-{random_string_generator}"

        return unique_order_id_generator(instance,new_slug=new_slug)

    return order_id
class OrderManager(models.Manager):
    def get_or_new(self,cart_obj=None,billing_profile=None):
        created=False
        order_qs=self.get_queryset().filter(cart=cart_obj,billing_profile=billing_profile,active=True).exclude(status='paid')
        if order_qs.exists() and order_qs.count()==1:
            order_obj=order_qs.first()
            created=False
        else:
            #old_order_qs=Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj,active=True)
            #if old_order_qs.exists():
            #    old_order_qs.update(active=False)
            order_obj=self.model.objects.create(cart=cart_obj,billing_profile=billing_profile)
            created=False
        return order_obj,created

class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile,on_delete=models.CASCADE)
    shipping_address =models.ForeignKey(Address,on_delete=models.SET_NULL,null=True,related_name='shipping_address')
    billing_address =models.ForeignKey(Address,on_delete=models.SET_NULL,null=True,related_name='billing_address')
    order_id    =   models.CharField(max_length=120,blank=True)
    cart        =   models.ForeignKey(Cart,on_delete=models.SET_NULL,null=True)
    status      =   models.CharField(max_length=120,default='created',choices=ORDER_STATUS_CHOICES)
    #shipping_total
    active      =   models.BooleanField(default=True)
    shipping_total =   models.DecimalField(decimal_places=2,default=5.99,max_digits=100)
    total          =   models.DecimalField(decimal_places=2,default=5.99,max_digits=100)
    order   =   models.BooleanField(default=True)


    objects = OrderManager() ##extending the default manager
    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total=self.cart.total
        shipping_total=self.shipping_total
        new_total=float(cart_total)+float(shipping_total)
        self.total=new_total
        self.save()
        return new_total


    def check_done(self):
        billing_profile=self.billing_profile
        shipping_address=self.shipping_address
        billing_address=self.billing_address
        total=self.total
        if billing_profile and shipping_address and billing_address and total>0:
            return True
        return False


    def mark_paid(self):
        if self.check_done():
            self.status='paid'
            self.save()
        return self.status


def order_pre_save_receiver(sender=None,instance=None,*args,**kwargs):
    if not instance.order_id :
        instance.order_id=unique_order_id_generator(instance)
    qs=Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)

pre_save.connect(order_pre_save_receiver,sender=Order) #but never do in the pre save


def post_save_cart_total(sender,instance,created,*args,**kwargs):
    if not created: #is the function is running reight after creating the object
        cart_obj=instance
        cart_total=cart_obj.total
        cart_id=cart_obj.id
        qs=Order.objects.filter(cart__id=cart_id)
        if qs.exists() and qs.count()==1:
            order_obj=qs.first()
            order_obj.update_total()


post_save.connect(post_save_cart_total,sender=Cart)#user instance.save() on post save



def post_save_order(sender,instance,created,*args,**kwargs):
    if created: ##is this function running right after the object was created
    ##if so then go ,nor do not do anythig
        instance.update_total()

post_save.connect(post_save_order,sender=Order)
