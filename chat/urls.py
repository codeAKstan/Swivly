from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('start/<int:recipient_id>/', views.start_conversation, name='start_conversation'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
]
