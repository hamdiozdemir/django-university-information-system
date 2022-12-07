from django.urls import path
from . import views

app_name = "overviews"

urlpatterns = [
    path('students_list/', views.StudentsListView.as_view(), name="students_list"),
    path('departments_list/', views.DepartmentsListView.as_view(), name="departments_list"),
    path('curriculum/<int:dep_id>', views.curriculum_view, name="curriculum"),
    path('students_list/<int:pk>/', views.StudentsDetailView.as_view()),

]
