from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Product
from django.http import Http404
# Create your views here.

class ProductListView(ListView):
    queryset=Product.objects.all()
    template_name='products/product_list.html'

    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data(*args,**kwargs)
        print(context)
        return context

    def get_queryset(self,*args,**kwargs):
        return Product.objects.all()

def product_list_view(request):
    queryset=Product.objects.all()
    context={
        'object_list':queryset
    }
    return render(request,'products/product_list.html',context)



class PostDetailView(DetailView):
     queryset=Product.objects.all()
     template_name='products/product_detail.html'

     def get_object(self,*args,**kwargs):
         slug=self.kwargs.get('pk')
         product=Product.objects.get(pk=pk)
         return product
     def get_context_data(self,*args,**kwargs):
         context=super().get_context_data(*args,**kwargs)
         print(context)
         return context

     def get_queryset(self,*args,**kwargs):
         return Product.objects.all()


def post_detail_view(request,pk=None):
    object=get_object_or_404(Product,pk=pk )
    context={
    'object':object
    }
    return render(request,'products/product_detail.html',context)


class ProductDetailSlugView(DetailView):
    queryset=Product.objects.all()
    template_name='products/product_detail.html'


    def get_context_data(self,*args,**kwargs):
        request=self.request
        context=super().get_context_data(*args,**kwargs)
        cart_obj,new_obj=Cart.objects.new_or_get(request)
        context['cart']=cart_obj
        return context

    def get_object(self,*args,**kwargs):
        request=self.request
        slug=self.kwargs.get('slug')
        #instance=get_object_or_404(slug=slug,active=True)
        try:
            instance=Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404('Not Fount')
        except Product.MultipleObjectsReturned:
            qs=Product.objects.filter(slug=slug)
            if qs.exists() and qs.count() >=1:
                instance=qs.first()
        except:
            raise Http404('Ummmm')

        return instance
