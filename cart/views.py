from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from registration.models import Product
from .cart import Cart
from .forms import AddressForm
from decimal import Decimal
from django.contrib.auth.models import User
from .models import Configuration
# Create your views here.

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id =product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

@login_required
def checkout(request):
    cart = Cart(request)

    configuration = Configuration.objects.first()
    delivery_fee = configuration.delivery_fee if configuration else Decimal('5.00')

    
    subtotal = sum(Decimal(item['product'].price) * item['quantity'] for item in cart)
    total = subtotal + delivery_fee

    # Handle address form
    if request.method == 'POST':
        address_form = AddressForm(request.POST, instance=request.user.profile)
        if address_form.is_valid():
            address_form.save()
            return redirect('cart:checkout')  # Refresh the page after saving
    else:
        address_form = AddressForm(instance=request.user.profile)

    # Render checkout page
    context = {
        'cart': cart,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'total': total,
        'address_form': address_form,
    }
    return render(request, 'cart/checkout.html', context)