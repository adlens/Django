from django.shortcuts import render
from django.db.models import Q, F
from store.models import Product, OrderItem


def say_hello(request):
    queryset = OrderItem.objects.values("product_id").distinct()
    queryset2 = Product.objects.filter(id__in=queryset).order_by("title")

    return render(request, "hello.html", {"name": "Mosh", "products": list(queryset2)})
