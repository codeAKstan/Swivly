from django.contrib.auth.models import User

def admin_user(request):
    try:
        admin = User.objects.filter(is_superuser=True).first()
        return {'admin': admin}
    except User.DoesNotExist:
        return {'admin': None}
