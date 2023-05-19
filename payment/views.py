from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from basket.basket import Basket
import stripe


@login_required
def BasketView(request):
    basket = Basket(request)
    total = str(basket.get_total_price())
    total_rp = total.replace('.', '')
    total = int(total_rp)

    return render(request, "payment/home.html")


@login_required
def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, "payment/orderplaced.html")
