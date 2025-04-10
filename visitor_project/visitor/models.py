from django.db import models
from django.utils import timezone

class BlockedVisitor(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    company = models.CharField(max_length=100)
    reason = models.TextField()
    blocked_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.phone_number})"

class Employee(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    employee_id = models.CharField(max_length=50)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.employee_id})"

class Visitor(models.Model):
    COMPANY_CHOICES = [
        ('Wyzmindz', 'Wyzmindz'),
        ('Transscon', 'Transscon'),
        ('Asteya Services', 'Asteya Services'),
        ('YOCOYA Technologies', 'YOCOYA Technologies'),
    ]

    PURPOSE_CHOICES = [
        ('Work', 'Work'),
        ('Interview', 'Interview'),
        ('Meeting', 'Meeting'),
        ('Appointment', 'Appointment'),
        ('Delivery', 'Delivery'),
        ('Service', 'Service'),
        ('Others', 'Others'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('blocked', 'Blocked'),
        ('checked_out', 'Checked Out'),
    ]

    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    photo = models.TextField(blank=True, null=True)  # Base64 encoded photo
    company = models.CharField(max_length=100, choices=COMPANY_CHOICES)
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    employee_id = models.CharField(max_length=50, blank=True, null=True)
    person_to_meet = models.CharField(max_length=100, blank=True, null=True)
    host_phone = models.CharField(max_length=15, blank=True, null=True)
    host_email = models.EmailField(blank=True, null=True)
    check_in_time = models.DateTimeField(default=timezone.now)
    check_out_time = models.DateTimeField(blank=True, null=True)
    scheduled_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    host_approval_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('scheduled', 'Scheduled Later')
    ], default='pending')
    scheduled_date = models.DateTimeField(null=True, blank=True)
    host_comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.company} ({self.check_in_time.strftime('%Y-%m-%d %H:%M')})"

    class Meta:
        ordering = ['-check_in_time']
