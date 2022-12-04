from django.shortcuts import render
from registrations.models import Students

def home_view(request):
    active_student_number = len(Students.objects.filter(status="Active"))

    data = {"active_students":active_student_number}
    return render(request,"home.html", context=data)