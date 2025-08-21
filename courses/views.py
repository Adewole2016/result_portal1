from django.shortcuts import render, get_object_or_404, redirect
from .models import Department, Course
from .forms import DepartmentForm, CourseForm
from results.models import Session     # ✅ Correct source of Session
# Department Views
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'courses/department_list.html', {'departments': departments})

def department_add(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses:department_list')
    else:
        form = DepartmentForm()
    return render(request, 'courses/department_form.html', {'form': form, 'title': 'Add Department'})

def department_edit(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('courses:department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'courses/department_form.html', {'form': form, 'title': 'Edit Department'})

def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    return redirect('courses:department_list')


# Course Views
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_add(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses:course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Add Course'})

def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses:course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Edit Course'})

def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    return redirect('courses:course_list')
from django.shortcuts import render
from .models import Department, Course

def manage_courses_departments(request):
    departments = Department.objects.all()
    courses = Course.objects.all()
    return render(request, 'courses/manage.html', {
        'departments': departments,
        'courses': courses
    })
from django.views.generic import ListView
from .models import Department, Course

class DepartmentListView(ListView):
    model = Department
    template_name = 'courses/department_list.html'
    context_object_name = 'departments'

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
from django.shortcuts import render

def system_settings_view(request):
    return render(request, 'accounts/system_settings.html')

from django.shortcuts import render
from .models import Department, Course

def manage_departments_courses(request):
    departments = Department.objects.all()
    courses = Course.objects.all()
    return render(request, 'courses/manage_departments_courses.html', {
        'departments': departments,
        'courses': courses,
    })
from django.shortcuts import render
from .models import Department, Course

def manage_departments_courses(request):
    departments = Department.objects.all()
    courses = Course.objects.all()
    return render(request, "courses/manage_departments_courses.html", {
        "departments": departments,
        "courses": courses
    })
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Department, Course
from .forms import DepartmentForm, CourseForm

def add_department(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department added successfully.")
            return redirect('courses:manage_departments_courses')
    else:
        form = DepartmentForm()
    return render(request, 'courses/add_department.html', {'form': form})

def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Course added successfully.")
            return redirect('courses:manage_departments_courses')
    else:
        form = CourseForm()
    return render(request, 'courses/add_course.html', {'form': form})

from django.shortcuts import get_object_or_404
from .models import Department, Course
from .forms import DepartmentForm, CourseForm
from django.contrib import messages

def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully.")
            return redirect('courses:manage_departments_courses')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'courses/edit_department.html', {'form': form})

def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    messages.success(request, "Department deleted successfully.")
    return redirect('courses:manage_departments_courses')

def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully.")
            return redirect('courses:manage_departments_courses')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/edit_course.html', {'form': form})

def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course.delete()
    messages.success(request, "Course deleted successfully.")
    return redirect('courses:manage_departments_courses')

def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('courses:manage_departments_courses')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'courses/edit_department.html', {'form': form})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from results.models import Semester
from .forms import SessionForm, SemesterForm

def manage_sessions_semesters(request):
    sessions = Session.objects.all().order_by('-id')
    semesters = Semester.objects.all().order_by('-id')
    return render(request, 'courses/manage_sessions_semesters.html', {
        'sessions': sessions,
        'semesters': semesters,
    })


def add_session(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Session added successfully.")
            return redirect('courses:manage_sessions_semesters')
    else:
        form = SessionForm()
    return render(request, 'courses/add_session.html', {'form': form})


def edit_session(request, pk):
    session = get_object_or_404(Session, pk=pk)
    if request.method == 'POST':
        form = SessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, "Session updated successfully.")
            return redirect('courses:manage_sessions_semesters')
    else:
        form = SessionForm(instance=session)
    return render(request, 'courses/edit_session.html', {'form': form})


def delete_session(request, pk):
    session = get_object_or_404(Session, pk=pk)
    session.delete()
    messages.success(request, "Session deleted successfully.")
    return redirect('courses:manage_sessions_semesters')


# Similar for Semester
def add_semester(request):
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Semester added successfully.")
            return redirect('courses:manage_sessions_semesters')
    else:
        form = SemesterForm()
    return render(request, 'courses/add_semester.html', {'form': form})


def edit_semester(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    if request.method == 'POST':
        form = SemesterForm(request.POST, instance=semester)
        if form.is_valid():
            form.save()
            messages.success(request, "Semester updated successfully.")
            return redirect('courses:manage_sessions_semesters')
    else:
        form = SemesterForm(instance=semester)
    return render(request, 'courses/edit_semester.html', {'form': form})


def delete_semester(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    semester.delete()
    messages.success(request, "Semester deleted successfully.")
    return redirect('courses:manage_sessions_semesters')

# courses/views.py
from django.shortcuts import render
from .models import Course

def course_list(request):
    courses = Course.objects.select_related('department', 'lecturer').all().order_by('code')
    return render(request, 'courses/course_list.html', {'courses': courses})
