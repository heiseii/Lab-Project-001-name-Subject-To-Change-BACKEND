from django.urls import path
from . import views

urlpatterns = [
path ('register/', views.register_api, name='register'),
path ('login/', views.login_api, name='login'),
path ('logout/', views.logout_api, name='logout'),
]