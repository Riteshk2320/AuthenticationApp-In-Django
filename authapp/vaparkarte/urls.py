from django.contrib import admin
from django.urls import path,include
from vaparkarte import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.loginuser, name='login'),
    path('register', views.registeruser, name='register'),
    path('forgot', views.forgot_pass, name='forgot_pass'),
    path('change/<token>/', views.change_pass, name='change_pass'),
    path('logout', views.logoutuser, name='logout'),
]