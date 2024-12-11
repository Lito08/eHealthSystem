from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Admin panel URL
    path('admin/', admin.site.urls),

    # User authentication URLs
    path('login/', views.matric_login, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Resident management URLs
    path('create_resident/', views.create_resident, name='create_resident'),

    # AJAX endpoints
    path('get_rooms/', views.get_rooms, name='get_rooms'),  # Fetch rooms based on block and level
    path('update_matric_id/', views.update_matric_id, name='update_matric_id'),  # Update matric ID dynamically

    # Home page
    path('', views.home, name='home'),
]
