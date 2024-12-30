from celery import shared_task
from django.core.mail import EmailMessage
from .utils import generate_pdf

@shared_task
def send_order_confirmation_email(user_email, order_id):
    # Delay the import to avoid circular dependency
    from .models import Order  
    order = Order.objects.get(id=order_id)
    
    # Generate PDF invoice
    pdf_file = generate_pdf(order)

    # Set up the email
    subject = "Order Confirmation"
    message = f"Thank you for your order. Your order ID is {order_id}."
    from_email = "noreply@swivly.com"
    recipient_list = [user_email]

    # Create and send the email with attachment
    email = EmailMessage(subject, message, from_email, recipient_list)
    email.attach(f'order_{order.id}.pdf', pdf_file.read(), 'application/pdf')
    email.send()

@shared_task
def send_payment_confirmation_email(user_email, order_id):
    from .models import Order
    order = Order.objects.get(id=order_id)
    
    # Generate PDF invoice
    pdf_file = generate_pdf(order)

    # Set up the email
    subject = "Payment Confirmation"
    message = f"Your payment for order ID {order_id} has been successfully processed."
    from_email = "noreply@swivly.com"
    recipient_list = [user_email]

    # Create and send the email with attachment
    email = EmailMessage(subject, message, from_email, recipient_list)
    email.attach(f'order_{order.id}.pdf', pdf_file.read(), 'application/pdf')
    email.send()
