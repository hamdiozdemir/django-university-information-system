from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from .models import Faculties, Departments, AcademicStaff, Students, Curriculums, InstructionalPlan
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


class RegistrationHomeView(TemplateView):
    template_name = "registrations/index.html"


class AddFacultyView(SuccessMessageMixin, CreateView):
    model = Faculties
    fields = ["faculty"]
    success_url = reverse_lazy("registrations:index")
    success_message = "Faculty has been added successfully"


class AddDepartmentView(SuccessMessageMixin, CreateView):
    model = Departments
    fields = ["faculty","department"]
    success_url = reverse_lazy("registrations:index")
    success_message = "Department has been added successfully"


class AddAcademicStaffView(SuccessMessageMixin, CreateView):
    model = AcademicStaff
    fields = "__all__"
    success_url = reverse_lazy("registrations:index")
    success_message = "Academic Staff has been added successfully"


class AddStudentView(SuccessMessageMixin, CreateView):
    model = Students
    fields = ["first_name", "last_name", "faculty", "department", "status", "advisor"]
    success_url = reverse_lazy("registrations:index")
    success_message = "New student has been added successfully"


class AddCurriculumView(SuccessMessageMixin, CreateView):
    model = Curriculums
    fields = ["department", "term","code","title", "theortical_hours", "practical_hours", "ects", "course_type"]
    success_url = reverse_lazy("registrations:curriculums_form")
    success_message = "Course has added."

