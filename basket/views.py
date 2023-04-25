from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse
from store.models import Product
from .basket import Basket


def basket_summary(request):
    basket = Basket(request)
    print(basket)
    return render(request, "store/basket/summary.html", {"basket": basket})


def basket_add(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        product_qty = int(request.POST.get("productqty"))
        product = get_object_or_404(Product, id=product_id)
        basketqty = basket.__len__()
        basket.add(product=product, qty=product_qty)
        response = JsonResponse({"qty": basketqty})
        return response
