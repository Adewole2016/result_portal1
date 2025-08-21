from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("matric_no", "user", "level", "department", "gender")
    search_fields = ("matric_no", "user__first_name", "user__last_name", "user__username")
    list_filter = ("level", "department", "gender")
    raw_id_fields = ("user",)

