from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Maps the root URL to my_view
    path('login/', views.login, name='login'),  # Maps the login URL to login view
    path('logout/', views.logout, name='logout'),  # Maps the logout URL to logout view
    path('goals/edit/<int:id>/', views.edit_goal, name='edit_goal'),  # Maps the edit goal URL to edit_goal view
    path('goals/add/', views.add_goal, name='add_goal'),  # Maps the add goal URL to add_goal view
    path('goals/delete/<int:id>/', views.delete_goal, name='delete_goal'),  # Maps the delete goal URL to delete_goal view
]
