import json
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Visitor, BlockedVisitor, Employee

def phone_verification(request):
    return render(request, 'visitor/phone_verification.html')

@csrf_exempt
def verify_phone(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        phone = data.get('phone')

        # Validate phone number format (10 digits)
        if not phone or not phone.isdigit() or len(phone) != 10:
            return JsonResponse({
                'status': 'error',
                'message': 'Please enter a valid 10-digit phone number'
            })

        # Check if phone number is blocked
        if BlockedVisitor.objects.filter(phone_number=phone).exists():
            return JsonResponse({
                'status': 'blocked',
                'message': 'Access denied. Please contact office.'
            })

        # Check if phone exists in different tables
        visitor, created = Visitor.objects.get_or_create(
            phone_number=phone,
            defaults={
                'name': '',
                'email': '',
                'status': 'pending'
            }
        )

        if Employee.objects.filter(phone_number=phone).exists():
            employee = Employee.objects.get(phone_number=phone)
            visitor.name = employee.name
            visitor.email = employee.email
            visitor.save()

        return JsonResponse({
            'status': 'success',
            'redirect_url': f'/visitor/form/?phone={phone}'
        })

    return JsonResponse({'status': 'error'}, status=400)

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def visitor_form(request):
    phone = request.GET.get('phone')
    if not phone:
        return redirect('phone_verification')

    visitor = get_object_or_404(Visitor, phone_number=phone)
    
    if request.method == 'POST':
        # Update visitor details
        visitor.name = request.POST.get('name')
        visitor.email = request.POST.get('email')
        visitor.company = request.POST.get('company')
        visitor.purpose = request.POST.get('purpose')
        visitor.photo = request.POST.get('photo')
        
        if request.POST.get('purpose') == 'Work':
            visitor.employee_id = request.POST.get('employee_id')
        else:
            visitor.person_to_meet = request.POST.get('person_to_meet')
            visitor.host_phone = request.POST.get('host_phone')
            visitor.host_email = request.POST.get('host_email')
            
            # Send email to host for approval
            if visitor.host_email:
                context = {
                    'visitor': visitor,
                    'approval_url': f"{request.build_absolute_uri('/visitor/approve/')}?id={visitor.id}",
                    'reject_url': f"{request.build_absolute_uri('/visitor/reject/')}?id={visitor.id}",
                    'schedule_url': f"{request.build_absolute_uri('/visitor/schedule/')}?id={visitor.id}"
                }
                
                html_message = render_to_string('visitor/email/approval_request.html', context)
                
                send_mail(
                    subject='Visitor Approval Request',
                    message='A visitor is waiting for your approval.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[visitor.host_email],
                    html_message=html_message
                )

        visitor.save()
        return redirect('success')

    # Check if visitor is an employee
    is_employee = Employee.objects.filter(phone_number=phone).exists()
    if is_employee:
        employee = Employee.objects.get(phone_number=phone)
        initial_data = {
            'name': employee.name,
            'email': employee.email,
            'employee_id': employee.employee_id
        }
    else:
        initial_data = {
            'name': visitor.name,
            'email': visitor.email
        }

    return render(request, 'visitor/visitor_form.html', {
        'visitor': visitor,
        'initial_data': initial_data,
        'is_employee': is_employee,
        'default_host': {
            'phone': '9603704353',
            'email': 'gadimutthisriya@gmail.com'
        }
    })

@csrf_exempt
def approve_visitor(request):
    visitor_id = request.GET.get('id')
    visitor = get_object_or_404(Visitor, id=visitor_id)
    visitor.host_approval_status = 'approved'
    visitor.save()
    
    # Send notification to visitor
    if visitor.email:
        send_mail(
            subject='Visit Approved',
            message='Your visit has been approved.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[visitor.email]
        )
    
    return JsonResponse({'status': 'success'})

@csrf_exempt
def reject_visitor(request):
    visitor_id = request.GET.get('id')
    visitor = get_object_or_404(Visitor, id=visitor_id)
    visitor.host_approval_status = 'rejected'
    visitor.host_comments = request.POST.get('comments', '')
    visitor.save()
    
    # Send notification to visitor
    if visitor.email:
        send_mail(
            subject='Visit Rejected',
            message=f'Your visit has been rejected.\nReason: {visitor.host_comments}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[visitor.email]
        )
    
    return JsonResponse({'status': 'success'})

@csrf_exempt
def schedule_visitor(request):
    visitor_id = request.GET.get('id')
    visitor = get_object_or_404(Visitor, id=visitor_id)
    visitor.host_approval_status = 'scheduled'
    visitor.scheduled_date = request.POST.get('scheduled_date')
    visitor.host_comments = request.POST.get('comments', '')
    visitor.save()
    
    # Send notification to visitor
    if visitor.email:
        send_mail(
            subject='Visit Scheduled',
            message=f'Your visit has been scheduled for {visitor.scheduled_date}.\nComments: {visitor.host_comments}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[visitor.email]
        )
    
    return JsonResponse({'status': 'success'})

def visitor_list(request):
    visitors = Visitor.objects.all().order_by('-check_in_time')
    return render(request, 'visitor/visitor_list.html', {'visitors': visitors})

def success(request):
    return render(request, 'visitor/success.html')

@csrf_exempt
def checkout_visitor(request, visitor_id):
    if request.method == 'POST':
        visitor = get_object_or_404(Visitor, id=visitor_id)
        visitor.check_out_time = timezone.now()
        visitor.status = 'checked_out'
        visitor.save()
        return JsonResponse({
            'status': 'success',
            'checkout_time': visitor.check_out_time.strftime('%Y-%m-%d %H:%M:%S')
        })
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def get_host_details(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        try:
            employee = Employee.objects.get(name__icontains=name)
            return JsonResponse({
                'status': 'success',
                'phone': employee.phone_number,
                'email': employee.email
            })
        except Employee.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Host not found'})
    return JsonResponse({'status': 'error'}, status=400)
