from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('get-location-info/', views.get_location_info, name='get_location_info'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='place_info/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='place_info/logout.html'), name='logout'),
]
