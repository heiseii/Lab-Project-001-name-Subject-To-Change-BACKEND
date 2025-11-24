from django.urls import path
from . import views

urlpatterns = [
path ('register/', views.register_api, name='register'),
path ('login/', views.login_api, name='login'),
path ('logout/', views.logout_api, name='logout'),

path ('conversations/create/', views.create_or_get_conversation, name= 'create_conversations'),
path ('user/<int:user_id>/conversations/', views.get_user_conversations, name='user_conversations'),
path ('conversations/<int:conversation_id>/messages/', views.get_messages, name= 'get_messages'),

path('search/', views.search_users, name='search_users'),
]