from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Sum

from registrations.models import Students, Departments, Curriculums, InstructionalPlan

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
    curriculum_data = Curriculums.objects.filter(department_id = dep_id).order_by('term')
    curriculum_hours_sum = curriculum_data.aggregate(Sum('theortical_hours'))
    practical_hours_sum = curriculum_data.aggregate(Sum('practical_hours'))
    ects_sum = curriculum_data.aggregate(Sum('ects'))
    var = {
        "curriculum_data":curriculum_data, "curriculum_hours_sum":curriculum_hours_sum,
        "practical_hours_sum":practical_hours_sum,
        "ects_sum":ects_sum
        }
    return render(request,"overviews/curriculum.html",context=var)


class StudentsDetailView(DetailView):
    model = Students



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inst_plan = InstructionalPlan.objects.filter(student_id = self.kwargs.get('pk')).order_by('curriculum__term')
        context["inst_plan"] = inst_plan
        return context
    