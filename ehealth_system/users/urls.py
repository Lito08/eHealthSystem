from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('create/', views.create_user, name='create_user'),  # Admin-only user creation
    path('list/', views.user_list, name='user_list'),  # Admin can list users
    path('get-rooms/', views.get_rooms, name='get_rooms'),  # Fetch rooms dynamically
]
