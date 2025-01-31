from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Announcement
from .forms import AnnouncementForm

# View Announcements (Residents & Admins)
@login_required
def announcement_list(request):
    announcements = Announcement.objects.order_by('-created_at')
    return render(request, 'announcements/announcement_list.html', {'announcements': announcements})

@login_required
def manage_announcements(request):
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to manage announcements.")
        return redirect('announcement_list')

    announcements = Announcement.objects.order_by('-created_at')
    return render(request, 'announcements/manage_announcements.html', {'announcements': announcements})

@login_required
def create_announcement(request):
    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to create announcements.")
        return redirect('announcement_list')

    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)  # Don't save yet
            announcement.created_by = request.user  # Assign the logged-in user
            announcement.save()  # Now save with the assigned user
            messages.success(request, "Announcement created successfully!")
            return redirect('manage_announcements')
    else:
        form = AnnouncementForm()

    return render(request, 'announcements/create_announcement.html', {'form': form})

# Edit Announcements (Only Superadmins & Admins)
@login_required
def edit_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)

    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to edit this announcement.")
        return redirect('announcement_list')

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, "Announcement updated successfully!")
            return redirect('announcement_list')
    else:
        form = AnnouncementForm(instance=announcement)

    return render(request, 'announcements/edit_announcement.html', {'form': form, 'announcement': announcement})

# Delete Announcements (Only Superadmins & Admins)
@login_required
def delete_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)

    if request.user.role not in ['superadmin', 'admin']:
        messages.error(request, "You are not authorized to delete this announcement.")
        return redirect('announcement_list')

    announcement.delete()
    messages.success(request, "Announcement deleted successfully!")
    return redirect('announcement_list')
