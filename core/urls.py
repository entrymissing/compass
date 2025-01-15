from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Maps the root URL to my_view
    path('login/', views.login, name='login'),  # Maps the login URL to login view
    path('logout/', views.logout, name='logout'),  # Maps the logout URL to logout view
]
