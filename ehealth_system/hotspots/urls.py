from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.manage_hotspots, name='manage_hotspots'),
    path('add/', views.add_hotspot, name='add_hotspot'),
    path('edit/<int:hotspot_id>/', views.edit_hotspot, name='edit_hotspot'),
    path('delete/<int:hotspot_id>/', views.delete_hotspot, name='delete_hotspot'),
    path('view/', views.view_hotspots, name='view_hotspots'),
]
