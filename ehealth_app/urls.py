
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload'),
    path('download/<int:file_id>/', views.download_file, name='download'),
    path('eligibility-check/', views.eligibility_check, name='eligibility_check'),
]
