from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Store - Каталог'
    ordering = ['price']

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_ID')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['categories'] = cache.get_or_set('categories', ProductCategory.objects.all(), 30)
        return context


@login_required
def basket_add(request, product_ID):
    Basket.create_or_update(product_ID, request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_ID):
    basket = Basket.objects.get(id=basket_ID)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
