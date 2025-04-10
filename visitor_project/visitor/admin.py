from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import redirect
from django.utils import timezone
from django.urls import path
from .models import Visitor, BlockedVisitor, Employee

@admin.register(BlockedVisitor)
class BlockedVisitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'company', 'blocked_date')
    search_fields = ('name', 'phone_number', 'email', 'company')
    ordering = ('-blocked_date',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee_id', 'phone_number', 'email', 'department')
    search_fields = ('name', 'employee_id', 'phone_number', 'email')
    ordering = ('name',)

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'purpose', 'person_to_meet', 'check_in_time', 'status', 'photo_preview')
    list_filter = ('status', 'company', 'purpose', 'check_in_time')
    search_fields = ('name', 'phone_number', 'email', 'person_to_meet')
    readonly_fields = ('check_in_time', 'check_out_time', 'photo_preview')
    ordering = ('-check_in_time',)

    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'phone_number', 'email', 'photo', 'photo_preview')
        }),
        ('Visit Details', {
            'fields': ('company', 'purpose', 'employee_id', 'person_to_meet', 'host_phone', 'host_email')
        }),
        ('Status Information', {
            'fields': ('status', 'check_in_time', 'check_out_time', 'scheduled_time')
        }),
    )

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', obj.photo)
        return "No photo"
    photo_preview.short_description = 'Photo'

    def approve_selected(self, request, queryset):
        for visitor in queryset:
            visitor.status = 'approved'
            visitor.scheduled_time = timezone.now()
            visitor.save()
            
            # Send message to visitor
            visitor_message = f"Your visit request has been approved. Please visit at {visitor.scheduled_time.strftime('%H:%M')}."
            print(f"Sending SMS to {visitor.phone_number}: {visitor_message}")
            
            # Send message to host
            host_message = f"{visitor.name} has been approved for {visitor.purpose} at {visitor.scheduled_time.strftime('%H:%M')}."
            if visitor.host_phone:
                print(f"Sending SMS to {visitor.host_phone}: {host_message}")
    
    def reject_selected(self, request, queryset):
        for visitor in queryset:
            visitor.status = 'rejected'
            visitor.save()
            
            # Send message to visitor
            visitor_message = "Sorry, your visit request has been rejected."
            print(f"Sending SMS to {visitor.phone_number}: {visitor_message}")
    
    def block_selected(self, request, queryset):
        for visitor in queryset:
            BlockedVisitor.objects.create(
                name=visitor.name,
                phone_number=visitor.phone_number,
                email=visitor.email,
                company=visitor.company,
                reason="Blocked by admin"
            )
            visitor.status = 'blocked'
            visitor.save()
            
            # Send message to visitor
            visitor_message = "Access denied. Please contact the office."
            print(f"Sending SMS to {visitor.phone_number}: {visitor_message}")

    approve_selected.short_description = "Approve selected visitors"
    reject_selected.short_description = "Reject selected visitors"
    block_selected.short_description = "Block selected visitors"

    actions = ['approve_selected', 'reject_selected', 'block_selected']

    class Media:
        css = {
            'all': ('admin/css/visitor_admin.css',)
        }
