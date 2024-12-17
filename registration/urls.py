from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'swivly'

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='registration:login'), name='logout'),
    path('', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name='profile')

]