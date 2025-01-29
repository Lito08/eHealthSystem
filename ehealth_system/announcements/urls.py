from django.urls import path
from . import views

urlpatterns = [
    path('', views.announcement_list, name='announcement_list'),
    path('manage/', views.manage_announcements, name='manage_announcements'),
    path('create/', views.create_announcement, name='create_announcement'),
    path('edit/<int:announcement_id>/', views.edit_announcement, name='edit_announcement'),
    path('delete/<int:announcement_id>/', views.delete_announcement, name='delete_announcement'),
]
