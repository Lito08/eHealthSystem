from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('profile/', views.view_profile, name='view_profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('manage/', views.manage_users, name='manage_users'),
    path('create/', views.create_user, name='create_user'),
    path('update/<int:user_id>/', views.update_user, name='update_user'),
    path('clear-room/<int:user_id>/', views.clear_room, name='clear_room'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('get-rooms/', views.get_rooms, name='get_rooms'),
    path('generate-matric-id/', views.generate_matric_id, name='generate_matric_id'),
]
