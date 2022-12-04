from django.shortcuts import render
from django.views.generic import ListView

from registrations.models import Students, Departments, Curriculums

# Create your views here.

class StudentsListView(ListView):
    model = Students
    context_object_name = "students_list"
    template_name = "overviews/students_list.html"

class DepartmentsListView(ListView):
    model = Departments
    context_object_name = "departments_list"
    template_name = "overviews/departments_list.html"

def curriculum_view(request, dep_id):
    data = Curriculums.objects.filter(department_id = dep_id)
    var = {"data":data}
    return render(request,"overviews/curriculum.html",context=var)