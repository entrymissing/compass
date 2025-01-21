from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('goals/edit/<int:id>/', views.edit_goal, name='edit_goal'),
    path('goals/add/', views.add_goal, name='add_goal'),
    path('goals/delete/<int:id>/', views.delete_goal, name='delete_goal'),
    path('goals/', views.all_goals, name='all_goals'),
]
