from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'swivly'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('shop/', views.market_place, name='shop'),
    path('shop/<slug:category_slug>/', views.product_list_or_index, name='shop_product_list_by_category'),
    path('shop/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('about/', views.about_us, name='about'),
    path('accommodation/', views.accommodation, name='accommodation'),
    path('add/', views.add_house, name='add_house'),
    path('accommdate/', views.accommodation_list, name='accommodation_list'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('edit/', views.edit, name='edit'),
    path('listing_summary/', views.listing_summary, name='listing_summary'),
    path('', views.product_list_or_index, name='product_list'),
    path('<slug:category_slug>/', views.product_list_or_index, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/upload/', views.add_product, name='add_product'),

]
