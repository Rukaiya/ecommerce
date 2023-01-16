from store.models import Product
from decimal import Decimal


class Basket():
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('session_key')

        if 'session_key' not in request.session:
            basket = self.session['session_key'] = {}

        self.basket = basket


    def add(self, product, quantity):
        product_id = product.id

        if product_id not in self.basket:
            self.basket[product_id] = { 'price': str(product.price), 'quantity': int(quantity) }

        self.save()

    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item


    def __len__(self):
        return sum(item['quantity'] for item in self.basket.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())

    def delete(self, product_id):
        product_id = str(product_id)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def save(self):
        self.session.modified = True
