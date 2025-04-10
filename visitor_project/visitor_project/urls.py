from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_visitor(request):
    return redirect('visitor_list')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_visitor),
    path('visitor/', include('visitor.urls')),
]
