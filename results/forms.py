
from django import forms
from courses.models import Department
from results.models import Session, Semester
from django import forms
from .models import GradingSystem
from results.models import Result


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['name', 'start_year', 'end_year', 'is_current']

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['session', 'semester', 'is_current']




class GradingSystemForm(forms.ModelForm):
    class Meta:
        model = GradingSystem
        fields = ['name', 'is_active']



class BroadsheetFilterForm(forms.Form):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label="Select Department",
        required=True,
        widget=forms.Select(attrs={
            "class": "form-control",
            "onchange": "this.form.submit()"
        })
    )
    session = forms.ModelChoiceField(
        queryset=Session.objects.all().order_by("-start_year"),
        empty_label="Select Session",
        required=True,
        widget=forms.Select(attrs={
            "class": "form-control",
            "onchange": "this.form.submit()"
        })
    )
    semester = forms.ModelChoiceField(
        queryset=Semester.objects.none(),
        empty_label="Select Semester",
        required=True,
        widget=forms.Select(attrs={
            "class": "form-control",
            "onchange": "this.form.submit()"
        })
    )
    level = forms.ChoiceField(
        choices=[('', 'Select Level'), ('100', '100'), ('200', '200'), ('300', '300'), ('400', '400')],
        required=False,
        widget=forms.Select(attrs={
            "class": "form-control",
            "onchange": "this.form.submit()"
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "session" in self.data:
            try:
                session_id = int(self.data.get("session"))
                self.fields["semester"].queryset = Semester.objects.filter(
                    session_id=session_id
                ).order_by("semester")
            except (ValueError, TypeError):
                self.fields["semester"].queryset = Semester.objects.none()
        elif "session" in self.initial:
            session = self.initial.get("session")
            self.fields["semester"].queryset = Semester.objects.filter(
                session=session
            ).order_by("semester")



from django import forms
from courses.models import Course
from results.models import Session, Semester

class ScoreUploadForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    session = forms.ModelChoiceField(queryset=Session.objects.all())
    semester = forms.ModelChoiceField(queryset=Semester.objects.all())
    score_file = forms.FileField()

class ResultUploadForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'ca_score', 'exam_score']  # exclude course, semester

    def __init__(self, *args, **kwargs):
        self.course = kwargs.pop('course')
        self.semester = kwargs.pop('semester')
        self.uploaded_by = kwargs.pop('uploaded_by')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.course = self.course
        instance.semester = self.semester
        instance.uploaded_by = self.uploaded_by
        if commit:
            instance.save()
        return instance

