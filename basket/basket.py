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

        self.session.modified = True

    def __len__(self):
        return sum(item['quantity'] for item in self.basket.values())
