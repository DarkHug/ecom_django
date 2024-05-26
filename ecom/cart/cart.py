from store.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user in new, no session. Need to create
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Check if car available in all pages
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        # Logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        # Get ids from cart
        products_ids = self.cart.keys()

        # Use ids to lookup products in database model
        products = Product.objects.filter(id__in=products_ids)

        return products

    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # Get Cart
        ourcart = self.cart

        # Update Dictionary
        ourcart[product_id] = product_qty

        self.session.modified = True

        thing = self.cart
        return thing
