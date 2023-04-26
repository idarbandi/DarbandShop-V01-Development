from _decimal import Decimal

from store.models import Product


class Basket():
    """
    The Abstract basket class That can Be Inherited & Overwritten
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get("skey")
        if "skey" not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product, qty):
        """
            Adding and Updating the users basket Session data
        """
        product_id = product.id
        if product_id not in self.basket:
            self.basket[product_id] = {
                "price": str(product.price), "qty": int(qty)}
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
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
    
    def delete(self, product):
        """
            delete the basket item from session
        """
        product_id = str(product)
        if product_id in self.basket:
            del self.basket[product_id]
        self.save()
    
    def save(self):
        self.session.modified = True