from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model



User = get_user_model()

class Session(models.Model):
    name = models.CharField(max_length=20, unique=True)  # e.g., "2024/2025"
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_year"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_current:
            Session.objects.exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)


class Semester(models.Model):
    SEMESTER_CHOICES = [
        ("first", "First Semester"),
        ("second", "Second Semester"),
    ]

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("session", "semester")
        ordering = ["-session__start_year", "semester"]

    def __str__(self):
        return f"{self.session.name} - {self.get_semester_display()}"

    def save(self, *args, **kwargs):
        if self.is_current:
            Semester.objects.exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)


class GradingSystem(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class GradeScale(models.Model):
    grading_system = models.ForeignKey(GradingSystem, on_delete=models.CASCADE, related_name="scales")
    grade = models.CharField(max_length=2)  # A, B, C, D, E, F
    min_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    grade_point = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        unique_together = ("grading_system", "grade")
        ordering = ["-min_score"]

    def __str__(self):
        return f"{self.grade} ({self.min_score}-{self.max_score})"


class Result(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("submitted", "Submitted"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    ca_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(40)],
        help_text="Continuous Assessment score (0-40)"
    )
    exam_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(60)],
        help_text="Examination score (0-60)"
    )
    total_score = models.IntegerField(editable=False)
    grade = models.CharField(max_length=2, editable=False)
    grade_point = models.FloatField(editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="uploaded_results")
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_results")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "course", "semester")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.student.matric_no} - {self.course.code} - {self.total_score}"

    def save(self, *args, **kwargs):
        self.total_score = self.ca_score + self.exam_score
        self._calculate_grade()
        super().save(*args, **kwargs)

    def _calculate_grade(self):
        grading_system = GradingSystem.objects.filter(is_active=True).first()
        if grading_system:
            grade_scale = grading_system.scales.filter(
                min_score__lte=self.total_score,
                max_score__gte=self.total_score
            ).first()
            if grade_scale:
                self.grade = grade_scale.grade
                self.grade_point = grade_scale.grade_point
                return
        # Default grading if no system is active
        if self.total_score >= 75:
            self.grade, self.grade_point = "A", 4.0
        elif self.total_score >= 70:
            self.grade, self.grade_point = "AB", 3.5
        elif self.total_score >= 65:
            self.grade, self.grade_point = "B", 3.25
        elif self.total_score >= 60:
            self.grade, self.grade_point = "BC", 3.00
        elif self.total_score >= 55:
            self.grade, self.grade_point = "C", 2.75

        elif self.total_score >= 50:
            self.grade, self.grade_point = "CD", 2.50
        elif self.total_score >= 45:
            self.grade, self.grade_point = "D", 2.25


        elif self.total_score >= 40:
            self.grade, self.grade_point = "E", 2.00
        else:
            self.grade, self.grade_point = "F", 0.00


class StudentSemesterSummary(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    total_credit_units = models.IntegerField(default=0)
    total_grade_points = models.FloatField(default=0.0)
    gpa = models.FloatField(default=0.0)
    cgpa = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "semester")
        ordering = ["-semester__session__start_year", "-semester__semester"]

    def __str__(self):
        return f"{self.student.matric_no} - {self.semester} - GPA: {self.gpa}"

    def calculate_gpa(self):
        results = Result.objects.filter(
            student=self.student,
            semester=self.semester,
            status="approved"
        )
        total_credit_units = sum(r.course.credit_units for r in results)
        total_grade_points = sum(r.grade_point * r.course.credit_units for r in results)

        self.total_credit_units = total_credit_units
        self.total_grade_points = total_grade_points
        self.gpa = total_grade_points / total_credit_units if total_credit_units > 0 else 0.0

        summaries = StudentSemesterSummary.objects.filter(student=self.student).exclude(id=self.id)
        cumulative_credit_units = total_credit_units + sum(s.total_credit_units for s in summaries)
        cumulative_grade_points = total_grade_points + sum(s.total_grade_points for s in summaries)
        self.cgpa = cumulative_grade_points / cumulative_credit_units if cumulative_credit_units > 0 else 0.0
        self.save()
