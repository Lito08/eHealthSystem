from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('appointments/', include('appointments.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
]
