from _decimal import Decimal
from django.conf import settings
from backend.apps.catalogue.models import Product
from backend.apps.checkout.models import DeliveryOptions


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
            self.basket[product_id] = {"price": str(product.regular_price), "qty": qty}
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
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item["price"] = Decimal(item['price'])
            item["total_price"] = item['price'] * item['qty']
            yield item
            
    def get_subtotal_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
    
    def get_total_price(self):
        """
            Get The Basket data and count the total qty price
        """
        new_price = 0.00
        subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
            
        if "purchase" in self.session:
            new_price = DeliveryOptions.objects.get(id=self.session['purchase']['delivery_id']).delivery_price
            
        total = subtotal + Decimal(new_price)
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

    def basket_update_delivery(self, delivery_price=0):
        subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.basket.values()) 
        total = subtotal + Decimal(delivery_price)
        return total  
    
    def get_delivery_price(self):
        
        new_price = 0.00
        if "purchase" in self.session:
            new_price = DeliveryOptions.objects.get(id=self.session['purchase']['delivery_id']).delivery_price
        
        return new_price

    def clear(self):
        """
            Remove Basket From The Session
        """
        del self.session[settings.BASKET_SESSION_ID]
        del self.session['address']
        del self.session['purchase']
        self.save()

    def save(self):
        self.session.modified = True
