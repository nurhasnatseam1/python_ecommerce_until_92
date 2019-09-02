from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from accounts.models import GuestEmail
# Create your models here.

User=settings.AUTH_USER_MODEL
## 1 anonymous user can have 100,000 billing profile but only one of them will be active
## and on registered user can only have one billing profile not more thant that
class BillingProfileManager(models.Manager):
    def get_or_new(self,request):
        user=request.user
        billing_profile_created=False
        guest_email_id=request.session.get('guest_email_id')
        if user.is_authenticated:
            #logged in user checkot
            billing_profile,billing_profile_created=self.model.objects.get_or_create(user=user,email=user.email)
        elif guest_email_id is not None:
            #guest user checkout
            guest_email_obj=GuestEmail.objects.get(id=guest_email_id)
            billing_profile,billing_profile_created=self.model.objects.get_or_create(email=guest_email_obj.email)
        return billing_profile,billing_profile_created



class BillingProfile(models.Model):
    user        =   models.OneToOneField(User,null=True,blank=True,on_delete=models.SET_NULL)##beacuase i want to allow anyguest user to make any accounts
    email       =   models.EmailField()
    timestamp   =   models.DateTimeField(auto_now_add=True)
    update      =   models.DateTimeField(auto_now=True)
    active      =   models.BooleanField(default=True)
    objects     =   BillingProfileManager()
#   customer_id in Stripe or BrainTree
    def __str__(self):
        return str(self.id)




def user_created_receiver(sender,instance,created,*args,**kwargs):

    if created : ## and instance.email:
        BillingProfile.objects.get_or_create(user=instance,email=instance.email)




post_save.connect(user_created_receiver,sender=User)
