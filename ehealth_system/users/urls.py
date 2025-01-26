from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('create/', views.create_user, name='create_user'),
    path('list/', views.user_list, name='user_list'),
    path('get-rooms/', views.get_rooms, name='get_rooms'),
]
