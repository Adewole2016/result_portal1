from django.contrib import admin
from .models import Department, Course

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "created_at", "updated_at")
    search_fields = ("name", "code")
    list_filter = ("created_at", "updated_at")
    ordering = ("name",)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "credit_units", "department", "level", "semester", "lecturer", "created_at")
    search_fields = ("code", "title", "department__name", "lecturer__username")
    list_filter = ("department", "level", "semester", "lecturer")
    raw_id_fields = ("lecturer",)
    ordering = ("code",)



