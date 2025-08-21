from django import forms
from .models import Department, Course
from results.models import Session
from results.models import Semester




class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'title', 'credit_units', 'department', 'level', 'semester', 'lecturer', 'description']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'credit_units': forms.NumberInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'level': forms.NumberInput(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-select'}),
            'lecturer': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


from django import forms
from results.models import Session  # or from courses.models if that’s where it is

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['name','start_year', 'end_year']




class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['session', 'semester', 'is_current']

