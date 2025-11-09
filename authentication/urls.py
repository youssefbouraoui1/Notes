from django.urls import path
from .views import register, get_users

urlpatterns = [
    path('', register, name='create_user'),
    path('all',get_users, name = "get_users" )
]