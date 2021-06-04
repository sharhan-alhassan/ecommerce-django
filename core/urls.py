

from django.urls import path
from . import views

from django.views.generic import TemplateView

app_name = 'core'
urlpatterns = [
    # path('', views.item_list, name='item-list'),
    path('', TemplateView.as_view(template_name='home-page.html')),
    path('product/', TemplateView.as_view(template_name='product-page.html'), name='product'),
    path('checkout/', TemplateView.as_view(template_name='checkout-page.html'), name='checkout'),


]