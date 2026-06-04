
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('start/<str:agent_type>/', views.start_chat_view, name='start_chat'),
    path('session/<int:session_id>/', views.chat_room_view, name='chat_room'),

    path('session/<int:session_id>/send/', views.send_message_api, name='send_message'),
]