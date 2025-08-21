from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, AuditLog
from .forms import CustomUserCreationForm, UserUpdateForm
from django.http import JsonResponse
from django.contrib.auth.views import PasswordResetView


def login_view(request):
    """
    Custom login view with audit logging.
    Redirects users based on roles.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                # Log login action
                AuditLog.objects.create(
                    user=user,
                    action='login',
                    description=f'User {user.username} logged in',
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )

                messages.success(request, f'Welcome back, {user.get_full_name()}!')

                # Redirect based on role
                if user.is_admin:
                    return redirect('accounts:admin_dashboard')
                elif user.is_hod:
                    return redirect('accounts:hod_dashboard')
                elif user.is_lecturer:
                    return redirect('accounts:lecturer_dashboard')
                else:
                    return redirect('accounts:student_dashboard')
            else:
                messages.error(request, 'Your account is inactive. Contact administrator.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    """
    Logout with audit logging
    """
    AuditLog.objects.create(
        user=request.user,
        action='logout',
        description=f'User {request.user.username} logged out',
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )

    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required
def dashboard_view(request):
    """
    Redirect user to their specific dashboard
    """
    if request.user.is_admin:
        return redirect('accounts:admin_dashboard')
    elif request.user.is_hod:
        return redirect('accounts:hod_dashboard')
    elif request.user.is_lecturer:
        return redirect('accounts:lecturer_dashboard')
    else:
        return redirect('accounts:student_dashboard')


@login_required
def admin_dashboard(request):
    if not request.user.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('accounts:dashboard')

    context = {
        'total_users': User.objects.count(),
        'total_students': User.objects.filter(role='student').count(),
        'total_lecturers': User.objects.filter(role='lecturer').count(),
        'total_hods': User.objects.filter(role='hod').count(),
        'recent_activities': AuditLog.objects.select_related('user').order_by('-timestamp')[:10]
    }
    return render(request, 'accounts/admin_dashboard.html', context)

@login_required
def hod_dashboard(request):
    if not request.user.is_hod:
        messages.error(request, 'Access denied. HOD privileges required.')
        return redirect('accounts:dashboard')

    department = request.user.department
    print("DEBUG: Department object =", department)
    print("DEBUG: Department name =", getattr(department, 'name', None))

    context = {
        'department': department,
        'department_students': Student.objects.filter(department=department).count(),
        'department_lecturers': User.objects.filter(role='lecturer', department=department).count(),
    }
    return render(request, 'accounts/hod_dashboard.html', context)




from students.models import Student
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

@login_required
def student_dashboard(request):
    if not request.user.is_student:
        messages.error(request, 'Access denied. Student privileges required.')
        return redirect('accounts:dashboard')

    student = getattr(request.user, "student_profile", None)

    context = {
        "user": request.user,             # pass user explicitly for template
        #"student_profile": student_profile,
        "student": student,
        # Add other context variables here as needed, e.g. GPA, CGPA, results, etc.
    }

    return render(request, 'accounts/student_dashboard.html', context)


class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/user_create.html'
    success_url = reverse_lazy('accounts:admin_dashboard')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        AuditLog.objects.create(
            user=self.request.user,
            action='create',
            model_name='User',
            object_id=str(self.object.id),
            description=f'Created user: {self.object.username}',
            ip_address=get_client_ip(self.request),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )
        messages.success(self.request, f'User {self.object.username} created successfully.')
        return response


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')


@login_required
def user_list(request):
    if not request.user.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('accounts:dashboard')
    
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'accounts/user_list.html', {'users': users})


class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/user_create.html'
    success_url = reverse_lazy('accounts:admin_dashboard')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=True)  # Ensure user is saved
        AuditLog.objects.create(
            user=self.request.user,
            action='create',
            model_name='User',
            object_id=str(user.id),
            description=f'Created user: {user.username}',
            ip_address=get_client_ip(self.request),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )
        messages.success(self.request, f'User {user.username} created successfully.')
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error creating the user. Please check the fields.")
        return self.render_to_response(self.get_context_data(form=form))

from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_update.html'
    success_url = reverse_lazy('accounts:user_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('accounts:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, f'User {self.object.username} updated successfully.')
        return super().form_valid(form)

from django.contrib.admin.views.decorators import staff_member_required

@login_required
def system_settings_view(request):
    if not request.user.is_admin:
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('accounts:dashboard')
    return render(request, 'accounts/system_settings.html')
from django.shortcuts import render

def system_settings_view(request):
    return render(request, 'accounts/system_settings.html')
from results.models import GradingSystem

def manage_grading_systems(request):
    gradings = GradingSystem.objects.all()
    return render(request, "accounts/manage_grading_system.html", {"gradings": gradings})

from django.shortcuts import render, redirect
from results.models import GradingSystem
from django.contrib import messages

def manage_grading_systems(request):
    gradings = GradingSystem.objects.all()
    return render(request, "accounts/manage_grading_system.html", {"gradings": gradings})

def add_grading_system(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            GradingSystem.objects.create(name=name)
            messages.success(request, "Grading system added successfully.")
            return redirect("accounts:grading_system")
    return render(request, "accounts/manage_grading_system.html")

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from results.models import GradingSystem

def edit_grading_system(request, pk):
    grading_system = get_object_or_404(GradingSystem, pk=pk)
    
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            grading_system.name = name
            grading_system.save()
            messages.success(request, "Grading system updated successfully.")
            return redirect("accounts:grading_system")
    
    return render(request, "accounts/edit_grading_system.html", {"grading_system": grading_system})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CourseAllocation
from accounts.models import User
from courses.models import Course
from results.models import Session, Semester



@login_required
def manage_lecturers(request):
    lecturers = User.objects.filter(role='lecturer')
    return render(request, 'accounts/manage_lecturers.html', {
        'lecturers': lecturers,
    })


@login_required
def allocate_course(request):
    lecturers = User.objects.filter(role='lecturer')
    courses = Course.objects.all()
    sessions = Session.objects.all()
    semesters = Semester.objects.all()

    if request.method == 'POST':
        lecturer_id = request.POST.get('lecturer')
        course_id = request.POST.get('course')
        session_id = request.POST.get('session')
        semester_id = request.POST.get('semester')

        lecturer = get_object_or_404(User, id=lecturer_id)
        course = get_object_or_404(Course, id=course_id)
        session = get_object_or_404(Session, id=session_id)
        semester = get_object_or_404(Semester, id=semester_id)

        CourseAllocation.objects.create(
            lecturer=lecturer,
            course=course,
            session=session,
            semester=semester
        )
        messages.success(request, "Course allocated successfully.")
        return redirect('accounts:manage_lecturers')

    return render(request, 'accounts/allocate_course.html', {
        'lecturers': lecturers,
        'courses': courses,
        'sessions': sessions,
        'semesters': semesters
    })

@login_required
def delete_lecturer(request, lecturer_id):
    lecturer = get_object_or_404(User, id=lecturer_id)
    lecturer.delete()
    messages.success(request, "Lecturer deleted successfully.")
    return redirect('accounts:manage_lecturers')

@login_required
def manage_lecturers(request):
    lecturers = User.objects.filter(role='lecturer')
    return render(request, 'accounts/manage_lecturers.html', {'lecturers': lecturers})

from django.shortcuts import render, redirect, get_object_or_404
from results.models import GradingSystem
from .forms import GradingSystemForm

def grading_system_list(request):
    grading_systems = GradingSystem.objects.all()
    return render(request, 'accounts/grading_system_list.html', {'grading_systems': grading_systems})

def add_grading_system(request):
    if request.method == 'POST':
        form = GradingSystemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:grading_system')
    else:
        form = GradingSystemForm()
    return render(request, 'accounts/add_grading_system.html', {'form': form})

def edit_grading_system(request, grading_id):
    grading_system = get_object_or_404(GradingSystem, pk=grading_id)
    if request.method == 'POST':
        form = GradingSystemForm(request.POST, instance=grading_system)
        if form.is_valid():
            form.save()
            return redirect('accounts:grading_system')
    else:
        form = GradingSystemForm(instance=grading_system)
    return render(request, 'accounts/edit_grading_system.html', {
        'form': form,
        'grading_system': grading_system
    })

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from results.models import GradingSystem
from .forms import GradingSystemForm, GradeScaleFormSet

def grading_system_create(request):
    GradeScaleFormSet = inlineformset_factory(
        GradingSystem, GradeScale, form=GradeScaleForm,
        fields=('grade', 'min_score', 'max_score', 'grade_point'), extra=3, can_delete=True
    )

    if request.method == "POST":
        form = GradingSystemForm(request.POST)
        formset = GradeScaleFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            grading_system = form.save()
            formset.instance = grading_system
            formset.save()
            return redirect('your_success_url')  # Replace with your actual redirect
    else:
        form = GradingSystemForm()
        formset = GradeScaleFormSet()

    return render(request, 'add_grading_system.html', {'form': form, 'formset': formset})
def grading_system_update(request, pk):
    grading_system = get_object_or_404(GradingSystem, pk=pk)
    if request.method == 'POST':
        form = GradingSystemForm(request.POST, instance=grading_system)
        formset = GradeScaleFormSet(request.POST, instance=grading_system)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('grading_system_list')
    else:
        form = GradingSystemForm(instance=grading_system)
        formset = GradeScaleFormSet(instance=grading_system)
    return render(request, 'accounts/grading_system_form.html', {'form': form, 'formset': formset})

def grading_system_delete(request, pk):
    grading_system = get_object_or_404(GradingSystem, pk=pk)
    if request.method == 'POST':
        grading_system.delete()
        return redirect('grading_system_list')
    return render(request, 'accounts/grading_system_confirm_delete.html', {'object': grading_system})

def grading_system_list(request):
    systems = GradingSystem.objects.all()
    return render(request, 'accounts/grading_system_list.html', {'systems': systems})@login_required

from .models import CourseAllocation, User

def manage_lecturers(request):
    department = request.user.department

    # Get lecturers who have course allocations in this department
    lecturer_ids = CourseAllocation.objects.filter(
        lecturer__department=department
    ).values_list('lecturer_id', flat=True).distinct()

    lecturers = User.objects.filter(id__in=lecturer_ids)

    # All lecturers in department (if needed for dropdowns etc.)
    all_lecturers = User.objects.filter(role='lecturer', department=department)

    # Get all allocations for display
    allocations = CourseAllocation.objects.filter(
        lecturer__department=department
    )

    return render(request, 'accounts/manage_lecturers.html', {
        'lecturers': lecturers,
        'all_lecturers': all_lecturers,
        'allocations': allocations
    })



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import User
from courses.models import Course
from results.models import Session, Semester
from .models import CourseAllocation

@login_required
def assign_course(request, lecturer_id):
    lecturer = get_object_or_404(User, id=lecturer_id)
    courses = Course.objects.all()
    sessions = Session.objects.all()
    semesters = Semester.objects.all()

    if request.method == 'POST':
        selected_courses = request.POST.getlist('courses')
        semester_id = request.POST.get('semester')
        session_id = request.POST.get('session')

        semester = get_object_or_404(Semester, id=semester_id)
        session = get_object_or_404(Session, id=session_id)

        for course_id in selected_courses:
            CourseAllocation.objects.get_or_create(
                lecturer=lecturer,
                course_id=course_id,
                session=session,
                semester=semester
            )
        return redirect('accounts:manage_lecturers')

    return render(request, 'accounts/assign_course.html', {
        'lecturer': lecturer,
        'courses': courses,
        'semesters': semesters,
        'sessions': sessions,
    })

from django.shortcuts import get_object_or_404

def delete_allocation(request, allocation_id):
    allocation = get_object_or_404(CourseAllocation, id=allocation_id)
    lecturer_id = allocation.lecturer.id
    allocation.delete()
    return redirect('accounts:manage_lecturers')
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import CourseAllocation
from results.models import Result

@login_required
def lecturer_dashboard(request):
    lecturer = request.user

    allocations = CourseAllocation.objects.filter(lecturer=lecturer)
    assigned_courses_count = allocations.count()

    allocation_tuples = set(allocations.values_list('course_id', 'semester_id'))
    print("Allocation tuples:", allocation_tuples)  # <-- Debug here

    uploaded_results_tuples = set(
        Result.objects.filter(uploaded_by=lecturer)
        .values_list('course_id', 'semester_id').distinct()
    )
    print("Uploaded results tuples:", uploaded_results_tuples)  # <-- And here

    uploaded_results_count = len(allocation_tuples.intersection(uploaded_results_tuples))
    print("Intersection (uploaded results count):", uploaded_results_count)  # <-- And here

    pending_uploads_count = assigned_courses_count - uploaded_results_count
    if pending_uploads_count < 0:
        pending_uploads_count = 0

    context = {
        'allocations': allocations,
        'assigned_courses': assigned_courses_count,
        'uploaded_results': uploaded_results_count,
        'pending_uploads': pending_uploads_count,
    }

    return render(request, 'accounts/lecturer_dashboard.html', context)



from django.shortcuts import render
from datetime import date
from students.models import Student

def student_list(request):
    students = Student.objects.select_related('user', 'department').filter(user__role='student')

    # Calculate age for each student
    for student in students:
        if student.date_of_birth:
            today = date.today()
            student.age = today.year - student.date_of_birth.year - (
                (today.month, today.day) < (student.date_of_birth.month, student.date_of_birth.day)
            )
        else:
            student.age = None

    return render(request, 'accounts/student_list.html', {'students': students})

from django.shortcuts import render
from .models import User  # Assuming Lecturer is stored in User model with a role field

def lecturer_list(request):
    # If your User model has a role or user_type field
    lecturers = User.objects.filter(role='lecturer')  # adjust field name to yours
    return render(request, 'accounts/lecturer_list.html', {'lecturers': lecturers})






