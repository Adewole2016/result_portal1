# results/utils.py
import math
import pandas as pd
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from students.models import Student
from courses.models import Course
from .models import Result, Semester

REQUIRED_COLUMNS = {
    'matric': 'Matric No',
    'ca': 'CA Score (0-40)',
    'exam': 'Exam Score (0-60)',
}


def _clean_matric(value):
    if pd.isna(value):
        return None
    return str(value).strip()


def _to_float_or_none(value):
    if pd.isna(value):
        return None
    try:
        f = float(value)
        if math.isnan(f):
            return None
        return f
    except Exception:
        return None


def get_current_semester():
    """Fallback helper — adjust if your Semester API differs."""
    s = Semester.objects.filter(is_current=True).first()
    return s


def process_uploaded_scores(file_obj, course=None, semester=None, uploaded_by=None):
    """
    Process an Excel file matching the header:
    S/N  Matric No  Full Name  CA Score (0-40)  Exam Score (0-60)  Total  Grade  Remarks

    Returns a dict: { 'processed', 'updated', 'created', 'missing', 'row_errors', 'course', 'semester' }
    """
    summary = {
        'processed': 0,
        'created': 0,
        'updated': 0,
        'missing': [],      # matric numbers not found
        'row_errors': [],   # human readable row errors (first 200 chars each)
        'course': course,
        'semester': semester,
    }

    # read into DataFrame (pandas can read file-like objects from Django)
    try:
        df = pd.read_excel(file_obj, engine='openpyxl')
    except Exception as e:
        raise ValueError(f"Unable to read Excel file: {e}")

    # Ensure required columns exist (case-sensitive as in your header)
    for key, colname in REQUIRED_COLUMNS.items():
        if colname not in df.columns:
            raise ValueError(f"Required column '{colname}' not found in uploaded file.")

    # determine semester fallback
    if semester is None:
        semester = get_current_semester()
        if semester is None:
            raise ValueError("No current semester found; provide semester argument or set a current Semester.")

    # make sure course provided
    if course is None:
        raise ValueError("Course must be provided (either pass course argument or include course info in file).")

    # iterate rows
    for idx, row in df.iterrows():
        excel_row_number = idx + 2  # +2: pandas index 0 -> Excel row 2 if header row 1
        try:
            matric = _clean_matric(row[REQUIRED_COLUMNS['matric']])
            ca_raw = row[REQUIRED_COLUMNS['ca']]
            exam_raw = row[REQUIRED_COLUMNS['exam']]

            if not matric:
                summary['row_errors'].append(f"Row {excel_row_number}: missing matric number")
                continue

            ca_score = _to_float_or_none(ca_raw)
            exam_score = _to_float_or_none(exam_raw)

            if ca_score is None and exam_score is None:
                summary['row_errors'].append(f"Row {excel_row_number}: both CA and Exam missing for '{matric}'")
                continue

            # default missing numeric to 0? depends on policy. Here we require both present:
            if ca_score is None:
                summary['row_errors'].append(f"Row {excel_row_number}: missing/invalid CA for '{matric}'")
                continue
            if exam_score is None:
                summary['row_errors'].append(f"Row {excel_row_number}: missing/invalid Exam for '{matric}'")
                continue

            # validate ranges
            if not (0 <= ca_score <= 40):
                summary['row_errors'].append(f"Row {excel_row_number}: CA score {ca_score} out of range (0-40) for '{matric}'")
                continue
            if not (0 <= exam_score <= 60):
                summary['row_errors'].append(f"Row {excel_row_number}: Exam score {exam_score} out of range (0-60) for '{matric}'")
                continue

            # get student (case-insensitive matric search)
            try:
                student = Student.objects.get(matric_no__iexact=matric)
            except Student.DoesNotExist:
                summary['missing'].append(matric)
                continue

            # Create or update Result
            defaults = {
                'ca_score': ca_score,
                'exam_score': exam_score,
                'uploaded_by': uploaded_by,
                'status': 'submitted',
            }

            # Use update_or_create so Result.save() runs and computes grade/total
            obj, created = Result.objects.update_or_create(
                student=student,
                course=course,
                semester=semester,
                defaults=defaults
            )

            summary['processed'] += 1
            if created:
                summary['created'] += 1
            else:
                summary['updated'] += 1

        except Exception as e:
            # capture the error and continue
            msg = str(e)
            # keep message short in summary
            summary['row_errors'].append(f"Row {excel_row_number}: {msg}")

    return summary
