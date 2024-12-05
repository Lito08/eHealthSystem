from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ehealth_app import views  # Import views from the app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Add this line for the root URL
    path('upload/', views.upload_file, name='upload'),
    path('download/<int:file_id>/', views.download_file, name='download'),
    path('eligibility-check/', views.eligibility_check, name='eligibility_check'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serving media files in development
