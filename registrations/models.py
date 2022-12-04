from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Faculties(models.Model):
    faculty = models.CharField(max_length=100)
    faculty_code = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.faculty}"

    def save(self, *args, **kwargs):
        if self._state.adding:
            super().save(*args, **kwargs)
        self.faculty_code = self.pk+10
        super().save(*args, **kwargs)


class Departments(models.Model):
    faculty = models.ForeignKey(Faculties, on_delete=models.SET_NULL, null=True)
    department = models.CharField(max_length=100)
    department_code = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.department}"

    def save(self, *args, **kwargs):
        if self._state.adding:
            super().save(*args, **kwargs)
        self.department_code = self.pk+10
        super().save(*args, **kwargs)


class AcademicStaff(models.Model):
    TITLE_CHOICE = [
        ("Prof.Dr.", "Prof.Dr."),
        ("Assoc.Prof.Dr.", "Assoc.Prof.Dr."),
        ("Assist.Prof.Dr.", "Assist.Prof.Dr."),
        ("Instructor", "Instructor"),
        ("Res.Assist.", "Res.Assist."),
        ("Visitor Lecturer", "Visitor Lecturer")
    ]

    title = models.CharField(max_length=50, choices=TITLE_CHOICE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    faculty = models.ForeignKey(Faculties, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Departments, on_delete=models.SET_NULL, null=True)
    starting_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.title}"


class Students(models.Model):
    STATUS_CHOICE = [
        ("Active", "Active"),
        ("Passive", "Passive"),
        ("Graduated", "Graduated"),
        ("TransferedIn", "Transfered In"),
        ("TransferedOut", "Transfered Out"),
        ("Disenrolment", "Disenrolment")
    ]

    school_id = models.CharField(max_length=10, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    faculty = models.ForeignKey(Faculties, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Departments, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default="Active")
    advisor = models.ForeignKey(AcademicStaff, on_delete=models.SET_NULL, null=True, blank=True)
    enrolment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.school_id} - {self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if self._state.adding:
            super().save(*args, **kwargs)
        
        year = self.enrolment_date.strftime("%y")
        department_student_count = len(Students.objects.filter(department=self.department))
        self.school_id = f"{year} {self.faculty.pk+10} {self.department.pk+10} {department_student_count+100}"
        
        std = Students.objects.get(pk=self.pk)
        curr = Curriculums.objects.filter(department=self.department)
        for course in curr:
            InstructionalPlan.objects.create(student=std, curriculum=course)
        super().save(*args, **kwargs)


class Curriculums(models.Model):
    class Term(models.IntegerChoices):
        first = 1
        second = 2
        third = 3
        forth = 4
        fifth = 5
        sixth = 6
        seventh = 7
        eighth = 8

    TYPE_CHOICE = [
        ("C", "Compulsory"),
        ("E", "Elective")
    ]

    department = models.ForeignKey(Departments, on_delete=models.SET_NULL, null=True)
    term = models.IntegerField(choices=Term.choices)
    code = models.CharField(max_length=6, unique=True)
    title = models.CharField(max_length=50)
    theortical_hours = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(12)])
    practical_hours = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(12)])
    ects = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(12)])
    course_type = models.CharField(max_length=20, choices=TYPE_CHOICE)
    student = models.ManyToManyField(Students)

    def save(self, *args, **kwargs):
        if self._state.adding:
            super().save(*args, **kwargs)
        
        
        stds = Students.objects.filter(department = self.department)
        course = Curriculums.objects.get(pk=self.pk)
        for std in stds:
            InstructionalPlan.objects.create(student=std, curriculum=course)
        super().save(*args, **kwargs)


class InstructionalPlan(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    curriculum = models.ForeignKey(Curriculums, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2, default="NA")

