from _decimal import Decimal
from django.conf import settings
from store.models import Product


class Basket():
    """
        The Abstract basket class That can Be Inherited & Overwritten
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, product, qty, update=True):
        """
            Adding and Updating the users basket Session data
        """
        product_id = str(product.id)
        if product_id in self.basket:
            self.basket[product_id]["qty"] = qty
        else:
            self.basket[product_id] = {"price": str(product.price), "qty": qty}
        self.save()

    def __len__(self):
        """
        Get The Basket data and Count The Quantity of Items
        """
        return sum(item["qty"] for item in self.basket.values())

    def __iter__(self):
        """
            Collect The Product id in the session to Query The Database and Return Products
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item["price"] = Decimal(item['price'])
            item["total_price"] = item['price'] * item['qty']
            yield item

    def get_total_price(self):
        """
            Get The Basket data and count the total qty price
        """
        subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
        if subtotal == 0:
            shipping = Decimal(0.00)
        else:
            shipping = Decimal(11.50)
            
        total = subtotal + Decimal(shipping)
        return total

    def delete(self, product):
        """
            delete the basket item from session
        """
        product_id = str(product)
        if product_id in self.basket:
            del self.basket[product_id]
        self.save()

    def update(self, product, qty):
        """
            updates the basket in the session
        """
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        self.save()

    def clear(self):
        """
            Remove Basket From The Session
        """
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True
