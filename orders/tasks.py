from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_order_confirmation_email(user_email, order_id):
    subject = "Order Confirmation"
    message = f"Thank you for your order. Your order ID is {order_id}."
    from_email = "noreply@swivly.com"
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)

@shared_task
def send_payment_confirmation_email(user_email, order_id):
    subject = "Payment Confirmation"
    message = f"Your payment for order ID {order_id} has been successfully processed."
    from_email = "noreply@swivly.com"
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)
