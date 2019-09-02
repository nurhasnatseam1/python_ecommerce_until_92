from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import m2m_changed

User=settings.AUTH_USER_MODEL

# Create your models here.

class CartManager(models.Manager):
    def new(self,user=None):
        user_obj=None
        if user.is_authenticated:
            user_obj=user
        return self.model.objects.create(user=user_obj)

    def new_or_get(self,request):
        cart_id=request.session.get('cart_id',None)
        qs=self.get_queryset().filter(id=cart_id) #or self.model.objects.filter(id=cart_id)
        new_obj=False
        if qs.count()==1:
            new_obj=False
            cart_obj=qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user=request.user
                cart_obj.save()
        else:
            cart_obj=self.new(user=request.user)
            new_obj=True
            request.session['cart_id']=cart_obj.id
        return cart_obj,new_obj



class Cart(models.Model):
    products        =   models.ManyToManyField(Product,blank=True)
    user            =   models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    total           =   models.DecimalField(default=0.00,decimal_places=2,max_digits=100)
    timestamp       =   models.DateTimeField(auto_now_add=True)
    updated         =   models.DateTimeField(auto_now=True)



    objects         =   CartManager()#extending Cart manager
    def __str__(self):
        return f"{self.id}"



def cart_m2m_receiver(sender=None,instance=None,action=None,*args,**kwargs):
    if action=='post_add' or action =='post_remove' or action =='post_clear':
        products=instance.products.all()
        total=0
        for product in products:
            total+=product.price
        instance.total=total
        instance.save()




m2m_changed.connect(cart_m2m_receiver,sender=Cart.products.through)
