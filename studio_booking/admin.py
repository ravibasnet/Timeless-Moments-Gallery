from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, path
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from .models import BookingSession, AvailableSlot
from django import forms
from django.contrib import messages
from datetime import timedelta

class CompletedEventAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'session_type', 'get_dates', 'gallery_preview', 'testimonial_preview')
    list_filter = ('session_type', 'testimonial_approved')
    search_fields = ('client_name', 'client_email')
    readonly_fields = ('created_at', 'updated_at', 'gallery_preview', 'testimonial_preview')
    actions = ['approve_testimonial']

    def get_dates(self, obj):
        return ", ".join(obj.dates) if obj.dates else ""
    get_dates.short_description = 'Dates'

    def gallery_preview(self, obj):
        if obj.gallery_images and len(obj.gallery_images) > 0:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.gallery_images[0])
        return "No images"
    gallery_preview.short_description = 'Gallery Preview'

    def testimonial_preview(self, obj):
        return obj.testimonial[:100] + "..." if obj.testimonial else "No testimonial"
    testimonial_preview.short_description = 'Testimonial Preview'

    def approve_testimonial(self, request, queryset):
        queryset.update(testimonial_approved=True)
    approve_testimonial.short_description = "Approve testimonials"

    def get_queryset(self, request):
        return super().get_queryset(request).filter(status='completed')

    def has_add_permission(self, request):
        return False

class GalleryFeedbackAdmin(admin.ModelAdmin):
    list_display = ('booking_link', 'gallery_preview', 'testimonial_preview', 'testimonial_approved')
    list_filter = ('testimonial_approved',)
    readonly_fields = ('booking_link', 'created_at', 'updated_at', 'gallery_preview')
    fields = ('booking_link', 'gallery_images', 'gallery_preview', 'testimonial', 'testimonial_approved')
    
    def booking_link(self, obj):
        url = reverse('admin:studio_booking_bookingsession_change', args=[obj.id])
        return mark_safe(f'<a href="{url}">{obj.client_name} - {obj.get_session_type_display()}</a>')
    booking_link.short_description = 'Booking Session'
    
    def gallery_preview(self, obj):
        if obj.gallery_images and len(obj.gallery_images) > 0:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.gallery_images[0])
        return "No images"
    gallery_preview.short_description = 'Gallery Preview'
    
    def testimonial_preview(self, obj):
        return obj.testimonial[:100] + "..." if obj.testimonial else "No testimonial"
    testimonial_preview.short_description = 'Testimonial Preview'
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(status='completed')
    
    def has_add_permission(self, request):
        return False

@admin.register(BookingSession)
class BookingSessionAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'session_type', 'get_dates', 'status', 'gallery_feedback_link', 'created_at')
    list_filter = ('status', 'session_type')
    search_fields = ('client_name', 'client_email', 'location', 'special_requests')
    fieldsets = (
        ('Session Details', {
            'fields': ('client', 'session_type', 'dates', 'duration', 'location', 'status')
        }),
        ('Client Information', {
            'fields': ('client_name', 'client_email', 'client_phone', 'special_requests')
        }),
        ('Timestamps', {
            'fields': ('updated_at',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    actions = ['mark_as_completed']
    
    def get_dates(self, obj):
        return ", ".join(obj.dates) if obj.dates else ""
    get_dates.short_description = 'Dates'
    
    def gallery_feedback_link(self, obj):
        if obj.status == 'completed':
            url = reverse('admin:studio_booking_bookingsession_gallery', args=[obj.id])
            return mark_safe(f'<a href="{url}">Manage Gallery & Feedback</a>')
        return "Not completed"
    gallery_feedback_link.short_description = 'Gallery/Feedback'
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = "Mark selected sessions as completed"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/gallery/', self.admin_site.admin_view(self.gallery_feedback_view), 
                 name='studio_booking_bookingsession_gallery'),
        ]
        return custom_urls + urls
    
    def gallery_feedback_view(self, request, object_id):
        booking = get_object_or_404(BookingSession, pk=object_id)
        
        if request.method == 'POST':
            gallery_images = request.POST.getlist('gallery_images')
            testimonial = request.POST.get('testimonial', '')
            testimonial_approved = 'testimonial_approved' in request.POST
            
            booking.gallery_images = [img.strip() for img in gallery_images if img.strip()]
            booking.testimonial = testimonial
            booking.testimonial_approved = testimonial_approved
            booking.save()
            
            return HttpResponseRedirect(reverse('admin:studio_booking_bookingsession_changelist'))
        
        context = {
            'title': f'Manage Gallery & Feedback for {booking.client_name}',
            'original': booking,
            'gallery_images': booking.gallery_images,
            'testimonial': booking.testimonial,
            'testimonial_approved': booking.testimonial_approved,
            'opts': self.model._meta,
        }
        
        return TemplateResponse(request, 'admin/studio_booking/gallery_feedback.html', context)

class AvailableSlotRangeForm(forms.Form):
    start_date = forms.DateField(label='Start date')
    end_date = forms.DateField(label='End date')
    max_sessions = forms.IntegerField(label='Max sessions', min_value=1, initial=1)

@admin.register(AvailableSlot)
class AvailableSlotAdmin(admin.ModelAdmin):
    list_display = ('date', 'max_sessions')
    list_filter = ('date',)
    ordering = ('date',)
    change_list_template = 'admin/studio_booking/availableslot_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add-range/', self.admin_site.admin_view(self.add_range_view), name='studio_booking_availableslot_add_range'),
        ]
        return custom_urls + urls

    def add_range_view(self, request):
        context = dict(
            self.admin_site.each_context(request),
            opts=self.model._meta,
        )
        if request.method == 'POST':
            form = AvailableSlotRangeForm(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                max_sessions = form.cleaned_data['max_sessions']
                count = 0
                date = start_date
                while date <= end_date:
                    obj, created = AvailableSlot.objects.get_or_create(
                        date=date,
                        defaults={'max_sessions': max_sessions}
                    )
                    if created:
                        count += 1
                    date += timedelta(days=1)
                self.message_user(request, f"Created {count} slots.", messages.SUCCESS)
                return HttpResponseRedirect(reverse('admin:studio_booking_availableslot_changelist'))
        else:
            form = AvailableSlotRangeForm()
        context['form'] = form
        context['title'] = 'Add Available Slots for Date Range'
        return TemplateResponse(request, 'admin/studio_booking/availableslot_add_range.html', context)
