from django.urls import path
from . import views

app_name = 'accommodation'

urlpatterns =[
    path('', views.accommodation, name='accommodation'),
    path('add/', views.add_house, name='add_house'),
    path('list/', views.accommodation_list, name='accommodation_list'),
    path('<int:house_id>/', views.house_detail, name='house_detail'), 
    path('listing_summary/', views.listing_summary, name='listing_summary'),
    path('<int:house_id>/edit/', views.edit_listing, name='edit_listing'),
    path('<int:house_id>/delete/', views.delete_listing, name='delete_listing'),
]