from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg, Max, Min

from courses.models import Course, Department
from students.models import Student
from results.models import Result, Session, Semester, StudentSemesterSummary
from accounts.models import User

@login_required
def analytics_dashboard(request):
    """
    Analytics dashboard view
    """
    if not request.user.is_admin and not request.user.is_hod:
        messages.error(request, "Access denied. Admin or HOD privileges required.")
        return redirect("accounts:dashboard")

    context = {
        # Overall statistics
        "total_students": Student.objects.count(),
        "total_courses": Course.objects.count(),
        "total_departments": Department.objects.count(),
        "total_lecturers": User.objects.filter(role='lecturer').count(),
        "total_results_uploaded": Result.objects.count(),

        # Course performance statistics
        "course_performance": Course.objects.annotate(
            avg_score=Avg('result__total_score'),
            highest_score=Max('result__total_score'),
            lowest_score=Min('result__total_score'),
            num_results=Count('result')
        ).order_by('-avg_score')[:10],

        # Student performance trends (e.g., top 10 students by CGPA)
        "top_students_cgpa": StudentSemesterSummary.objects.values(
            'student__user__first_name', 'student__user__last_name', 'student__matric_no'
        ).annotate(
            avg_cgpa=Avg('gpa') # Assuming GPA is used for CGPA calculation over semesters
        ).order_by('-avg_cgpa')[:10],

        # Department-wise performance (average GPA)
        "department_performance": Department.objects.annotate(
            avg_gpa=Avg('student__studentsemestersummary__gpa')
        ).order_by('-avg_gpa'),

        # Current session and semester
        "current_session": Session.objects.filter(is_current=True).first(),
        "current_semester": Semester.objects.filter(is_current=True).first(),
    }

    return render(request, "analytics/analytics_dashboard.html", context)



