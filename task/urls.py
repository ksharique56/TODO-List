from django.contrib import admin
from django.urls import path, include
from task import views

urlpatterns = [
    path('', views.index, name='list'),
    path('update_task/<str:pk>/', views.updateTask, name='update_task'),
    path('delete/<str:pk>/', views.deleteTask, name='delete'),
    path('signup/', views.handleSignup, name='signup'),
    path('login/', views.handleLogin, name='login'),
    path('logout/', views.handleLogout, name='logout'),    
    path('changepass/', views.changePass, name='changepass'),    
]
