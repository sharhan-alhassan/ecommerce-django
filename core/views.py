

from django.db import models
from core.models import Item, Order, OrderItem

from django.views import generic
from django.utils import timezone

from django.shortcuts import redirect, render, get_object_or_404

# Create your views here.


class HomeView(generic.ListView):
    model = Item
    template_name = 'home.html'
    context_object_name = 'items'


class ItemDetailView(generic.DetailView):
    model = Item
    template_name = 'product.html'
    context_object_name = 'item'


def chechout(request):
    pass


def add_to_cart(request, slug):
    # First get the item from the Item list
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.create(item=item)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    # If the queryset exists
    if order_qs.exists():
        order = order_qs[0]

        # check if order item is in the order cart
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
    # Else if the queryset does not exists
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect('core:product', slug=slug)


def remove_from_cart(request, slug):
    pass


