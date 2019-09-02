from django.db import models
import random
import os
import string
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.db.models import Q
from django.shortcuts import reverse
# Create your models here.
def random_string_generator(size=10,chars=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size) )

def unique_slug_generator(instance,new_slug=None):
    if new_slug  is not None:
        slug=new_slug
    else:
        slug=slugify(instance.title)
    klass=instance.__class__
    print(klass)
    qs_exists=klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = f"{slug}-{random_string_generator(size=4)}"
        return unique_slug_generator(instance,new_slug=new_slug)
    return slug

def get_filename_ext(filename):
    base_name=os.path.basename(filename)
    name,ext=os.path.splittext(base_name)
    return ext


def upload_image_path(instance,filename):
    new_filename=random.randint(1,4523552126)
    return f"products/{instance.id}/{new_filename}.{get_filename_ext(filename)}"

class ProductManager(models.Manager): ## extending default model manager method
    def get_by_id(self,id):
        print(id)
        return self.model.objects.get(id=id) ##works as objects.filter and returns queryset // you can also do self.model.objects.filter(id=id)


    def search(self,query):
        lookups=Q(title__icontains=query)|Q(description__icontains=query)|Q(tag__title__icontains=query)
        return self.get_queryset().filter(lookups).distinct()


class Product(models.Model):
    title           =   models.CharField(max_length=120)
    slug            =   models.SlugField(blank=True,unique=True)
    description     =   models.TextField()
    price           =   models.DecimalField(decimal_places=2,max_digits=10,default=0.00)
    image           =   models.FileField(upload_to=upload_image_path,null=True,blank=True)
    timestamp       =   models.DateTimeField(auto_now_add=True,auto_now=False)
    active          =   models.BooleanField(default=True)
    featured        =   models.BooleanField(default=False)
    objects = ProductManager()

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('products:porduct_detail',kwargs={slug:self.slug})

def product_pre_save_receiver(sender=None,instance=None,*args,**kwargs): ##ringht before the the save method executes and saves in the database
    if not instance.slug:
        instance.slug=unique_slug_generator(instance)
pre_save.connect(product_pre_save_receiver,sender=Product)
