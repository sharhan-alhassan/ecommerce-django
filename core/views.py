
import stripe
 
from django.conf import settings

from django import forms
from django.db import models
from django.http import request
from django.http.response import HttpResponse
from core.models import Item, Order, OrderItem, BillingAddress

from django.views import generic
from django.utils import timezone

from django.shortcuts import redirect, render, get_object_or_404

from django.contrib import messages

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CheckoutForm
# Create your views here.


class HomeView(generic.ListView):
    model = Item    # This is same as: queryset=Item.objects.all()
    template_name = 'home.html'
    context_object_name = 'items'
    paginate_by = 10


class ItemDetailView(generic.DetailView):
    model = Item
    template_name = 'product.html'
    context_object_name = 'item'


class OrderSummaryView(LoginRequiredMixin, generic.View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)

        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have any order')
            return redirect('/')


class CheckoutView(generic.View):
    def get(self, *args, **kwargs):
        # get the checkout form (for the client) and render it into the context

        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'checkout.html', context)

    def post(self, *args, **kwargs):
        # deals with post request of the form (from the client)

        # instantiate the form and save the user data in 'form'
        form = CheckoutForm(self.request.POST or None)

        # first check if the user has an active
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)

            # check if form is valid: then you can used the saved data stored in 'cleaned_data'
            if form.is_valid():
                # then save the data in each corresponding fields
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                same_shipping_address = form.cleaned_data.get('same_shipping_address')
                save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')

                # Take all that info/data and save in the billing address table
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip,
                )
                # save the data
                billing_address.save()

                # Save the billing_address to the order
                order.billing_address = billing_address
                order.save()
                return redirect('core:checkout')
            messages.warning(self.request, 'Failed checkout')
            return redirect('core:checkout')

        # If they don't have an order
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order!")
            return redirect('core:order-summary')


class PaymentView(generic.View):
    def get(self, *args, **kwargs):
        return render(self.request, 'payment.html')


@login_required
def add_to_cart(request, slug):
    # First get the item from the Item list
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False,
    )

    # If the queryset exists
    if order_qs.exists():
        order = order_qs[0]

        # check if order item is in the order cart
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item is incremented!")
            return redirect('core:order-summary')
        # Else if order item not in order cart
        else:
            messages.info(request, "New item added to your cart!")
            order = order.items.add(order_item)
            return redirect('core:product', slug=slug)

    # Else if the queryset does not exists
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "New item added to your cart")
        return redirect('core:product', slug=slug)


@login_required
def remove_from_cart(request, slug):
    # Get the item
    item = get_object_or_404(Item, slug=slug)

    # checking if the user has an order
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False,
    )

    # If they do have an order
    if order_qs.exists():

        # Grab the order
        order = order_qs[0]

        # Filter the order by that specific item slug, and if it exists
        if order.items.filter(item__slug=item.slug).exists():

            # Grab the order from OrderItem
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False,
            )[0]
            # Then remove it
            order.items.remove(order_item)  # redundant //not needed
            order_item.delete()
            messages.warning(request, "This item is removed from your cart!")
            return redirect('core:order-summary')
        else:
            # The order does not contain this order item
            messages.warning(request, "This item is not in your cart!")
            return redirect('core:product', slug=slug)
    else:
        # the user doens't have an order
        messages.warning(request, "You do not have an active order!")
        return redirect('core:product', slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    # Get the item from the Items list
    item = get_object_or_404(Item, slug=slug)

    # checking if the user has an order
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False,
    )

    # If they do have an order
    if order_qs.exists():

        # Grab the order
        order = order_qs[0]

        # Filter the order by that specific item slug, and if it exists
        if order.items.filter(item__slug=item.slug).exists():

            # Grab the order from OrderItem
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False,
            )[0]
            if order_item.quantity > 1:
                # Then reduce the number of the item
                order_item.quantity -= 1
                order_item.save()   # Not deleting but saving after reducing it by 1
            else:
                order.items.remove(order_item)
                messages.warning(request, "This time is fully removed!")

            messages.warning(request, "This item is reduced!")
            return redirect('core:order-summary')
        else:
            # The order does not contain this order item
            messages.warning(request, "This item is not in your cart!")
            return redirect('core:order-summary')
    else:
        # the user doens't have an order
        messages.warning(request, "You do not have an active order!")
        return redirect('core:order-summary')

