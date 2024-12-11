from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.matric_login, name='login'),
    path('create_resident/', views.create_resident, name='create_resident'),
    path('logout/', views.logout_view, name='logout'),  # Handle logout
    path('get_rooms/', views.get_rooms, name='get_rooms'),  # New path for AJAX room fetching
    path('', views.home, name='home'),
]
