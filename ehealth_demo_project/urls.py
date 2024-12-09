from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ehealth_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ehealth_app.urls')),  # Include the app's URLs
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # Add login path
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),  # Add logout path
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
