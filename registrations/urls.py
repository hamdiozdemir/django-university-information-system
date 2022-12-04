from django.urls import path
from . import views

app_name = "registrations"

urlpatterns = [
    path('',views.RegistrationHomeView.as_view(), name="index"),
    path('faculties_form/',views.AddFacultyView.as_view(),name="faculties_form"),
    path('departments_form/',views.AddDepartmentView.as_view(), name="departments_form"),
    path('academicstaff_form/', views.AddAcademicStaffView.as_view(), name="academicstaff_form"),
    path('students_form/', views.AddStudentView.as_view(), name="students_form"),
    path('curriculums_form/', views.AddCurriculumView.as_view(), name="curriculums_form"),
    # path('curriculum/<int:depid>/',views.deneme, name="deneme"),




    
]
