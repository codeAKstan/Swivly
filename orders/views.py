from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from cart.cart import Cart
from paystackapi.paystack import Paystack
from paystackapi.transaction import Transaction
from decimal import Decimal

paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)

@login_required
def place_order(request):
    cart = Cart(request)

    # Create an order
    order = Order.objects.create(
        user=request.user,
        total_price=sum(item['product'].price * item['quantity'] for item in cart)
    )
    
    # Create order items
    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            price=item['product'].price,
            quantity=item['quantity']
        )
    
    # Clear the cart
    cart.clear()

    # Initialize Paystack Payment
    # Convert to kobo (Paystack expects amounts in kobo)
    total_amount = int(order.total_price * 100)  
    # Redirect URL after payment
    callback_url = request.build_absolute_uri('/orders/payment/verify/')  
    response = Transaction.initialize(
        reference=f"ORDER-{order.id}",# Redirect URL after payment
        amount=total_amount,
        email=request.user.email,
        callback_url=callback_url
    )

    if response['status']:
        # Redirect to Paystack payment page
        return redirect(response['data']['authorization_url'])
    else:
        # Handle payment initialization failure
        return render(request, 'orders/payment_failed.html', {'error': response['message']})


@login_required
def verify_payment(request):
    reference = request.GET.get('reference')
    response = Transaction.verify(reference)
    
    if response['status']:
        # Mark order as paid
        order_id = reference.split('-')[1]  # Extract order ID from reference
        order = get_object_or_404(Order, id=order_id, user=request.user)
        order.paid = True
        order.save()

        return render(request, 'orders/payment_success.html', {'order': order})
    else:
        # Payment verification failed
        return render(request, 'orders/payment_failed.html', {'error': response['message']})
