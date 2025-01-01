from django.urls import path
from . import views

app_name = 'accommodation'

urlpatterns =[
    path('', views.accommodation, name='accommodation'),
    path('add/', views.add_house, name='add_house'),
    path('list/', views.accommodation_list, name='accommodation_list'),
     path('<int:house_id>/', views.house_detail, name='house_detail'), 
]