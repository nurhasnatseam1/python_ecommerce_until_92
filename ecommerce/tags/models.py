from django.db import models
import string
from products.models import Product
from django.db.models.signals import pre_save
# Create your models here.
def random_string_generator(size=10,chars=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size) )

def unique_slug_generator(instance,new_slug=None):
    if new_slug  is not None:
        slug=new_slug
    else:
        slug=slugify(instance.title)
    klass=instance.__class__
    qs_exists=Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = f"{slug}-{random_string_generator(size=4)}"
        return unique_slug_generator(instance,new_slug=new_slug)
    return slug



class Tag(models.Model):
    title   =   models.CharField(max_length=120)
    slug    =   models.SlugField()
    timestamp = models.DateTimeField(auto_now_add=True)
    active  =   models.BooleanField(default=True)
    products=   models.ManyToManyField(Product,blank=True)


def tag_pre_save_receiver(sender=None,instance=None,*args,**kwargs): ##ringht before the the save method executes and saves in the database
    if not instance.slug:
        instance.slug=unique_slug_generator(instance)
pre_save.connect(tag_pre_save_receiver,sender=Tag)
