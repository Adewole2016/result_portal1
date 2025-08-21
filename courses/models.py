from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return f"{self.code} - {self.name}"


class Course(models.Model):
    SEMESTER_CHOICES = [
        ("first", "First Semester"),
        ("second", "Second Semester"),
    ]

    code = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    credit_units = models.PositiveIntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses")
    level = models.PositiveIntegerField()
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    lecturer = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role__in": ["lecturer", "hod", "admin"]},
        related_name="courses",
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("code", "semester", "level", "department")
        ordering = ["code"]
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return f"{self.code} - {self.title} ({self.department.name})"



