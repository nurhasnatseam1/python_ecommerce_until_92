from django.db import models
from billing.models import BillingProfile
# Create your models here.
ADDRESS_TYPES=(
('billing','BILLING'),
('shipping','SHIPPING'),
)


class Address(models.Model):
    address_type=models.CharField(max_length=120,choices=ADDRESS_TYPES)
    billing_profile=models.ForeignKey(BillingProfile,on_delete=models.CASCADE)
    address_line_1=models.CharField(max_length=120)
    address_line_2=models.CharField(max_length=120,null=True,blank=True)
    city=models.CharField(max_length=120)
    country=models.CharField(max_length=120,default='Bangladesh')
    state=models.CharField(max_length=120)
    postal_code=models.CharField(max_length=120)


    def __str__(self):
        return f"{self.billing_profile}"
