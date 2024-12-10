from django.urls import path
from . import views

app_name = 'swivly'

urlpatterns = [
    path('', views.index, name='index'),
]