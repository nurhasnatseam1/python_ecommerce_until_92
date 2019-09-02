from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product
from django.db.models import Q
# Create your views here.
class SearchListView(ListView):
    queryset=Product.objects.all()
    template_name='search/view.html'

    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data(*args,**kwargs)
        print(context)
        return context

    def get_queryset(self,*args,**kwargs):
        request=self.request
        method_dict=request.GET
        query=method_dict.get('q',None)
        if query is not None:
    #        lookups=Q(title__icontains=query)|Q(description__icontains=query)|Q()
    #        return Product.objects.filter(lookups)
            return Product.objects.search(query) ##beacuse i extended the model manager with the search method 
        return Product.objects.none()
