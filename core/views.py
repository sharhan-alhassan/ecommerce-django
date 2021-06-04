

from core.models import Item
from django.shortcuts import redirect, render

# Create your views here.


def item_list(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'item_list.html', context)
