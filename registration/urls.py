from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'swivly'

urlpatterns = [
    path('shop/', views.market_place, name='shop'),
    path('about/', views.about_us, name='about'),
    path('register', views.register, name='register'),
    path('', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name='profile'),
    path('edit/', views.edit, name='edit'),
    path('', views.product_list_or_index, name='product_list'),
    path('<slug:category_slug>/', views.product_list_or_index,
    name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

]