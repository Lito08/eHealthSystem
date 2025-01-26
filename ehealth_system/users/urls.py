from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('create/', views.create_user, name='create_user'),  # Admin-only user creation
    path('list/', views.user_list, name='user_list'),  # Admin-only user listing
    path('update/<int:user_id>/', views.update_user, name='update_user'),  # Admin-only user update
    path('get-rooms/', views.get_rooms, name='get_rooms'),  # Accessible by all authenticated users
    path('generate-matric-id/', views.generate_matric_id, name='generate_matric_id'),  # Accessible by all authenticated users
]
