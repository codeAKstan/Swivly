from decimal import Decimal
from django.conf import settings
from registration.models import Product

class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty cart in session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product):
        """
        Add a product to the cart.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 1, 
                'price': str(product.price)
            }
        self.save()

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        """
        Mark the session as modified to ensure changes are saved.
        """
        self.session.modified = True

    def __iter__(self):
        """
        Iterate over items in the cart and retrieve products from the database.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            cart_item = self.cart[str(product.id)]
            cart_item['product'] = product
            cart_item['price'] = Decimal(cart_item['price'])
            cart_item['total_price'] = cart_item['price']
            yield cart_item

    def __len__(self):
        """
        Count the number of unique products in the cart.
        """
        return len(self.cart)

    def get_total_price(self):
        """
        Calculate the total price of items in the cart.
        """
        return sum(
            Decimal(item['price']) for item in self.cart.values()
        )

    def clear(self):
        """
        Remove the cart from the session.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
