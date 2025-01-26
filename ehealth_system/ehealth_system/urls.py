from django.contrib import admin
from django.urls import include, path
from . import views
from django.contrib.auth.decorators import login_required
from users.views import dashboard

urlpatterns = [
    path('', views.home, name='home'),
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('appointments/', include('appointments.urls')),
    path('hostels/', include('hostels.urls')),
    path('dashboard/', login_required(dashboard), name='dashboard'),
]
