from django.contrib import admin
from .models import Session, Semester, GradingSystem, GradeScale, Result, StudentSemesterSummary

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("name", "start_year", "end_year", "is_current", "created_at")
    search_fields = ("name",)
    list_filter = ("is_current", "created_at")

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("session", "semester", "is_current", "created_at")
    search_fields = ("session__name", "semester")
    list_filter = ("is_current", "semester", "session")

from django.contrib import admin
from .models import GradingSystem, GradeScale

# 1. Create an inline admin for GradeScale
class GradeScaleInline(admin.TabularInline):
    model = GradeScale
    extra = 1  # Number of blank forms shown
    min_num = 1  # Minimum required
    verbose_name = "Grade Scale"
    verbose_name_plural = "Grade Scales"

# 2. Register GradingSystem with the inline
@admin.register(GradingSystem)
class GradingSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    inlines = [GradeScaleInline]


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "semester", "total_score", "grade", "grade_point", "status", "uploaded_by", "approved_by")
    search_fields = ("student__user__username", "student__matric_no", "course__code", "course__title")
    list_filter = ("semester", "course__department", "status", "grade", "uploaded_by", "approved_by")
    raw_id_fields = ("student", "course", "semester", "uploaded_by", "approved_by")
    readonly_fields = ("total_score", "grade", "grade_point")

@admin.register(StudentSemesterSummary)
class StudentSemesterSummaryAdmin(admin.ModelAdmin):
    list_display = ("student", "semester", "total_credit_units", "total_grade_points", "gpa", "cgpa")
    search_fields = ("student__user__username", "student__matric_no", "semester__session__name")
    list_filter = ("semester", "student__department")
    raw_id_fields = ("student", "semester")


