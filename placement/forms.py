from django import forms
from .models import Student, Company


# =========================
# STUDENT FORM
# =========================
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name',
            'register_no',
            'department',
            'cgpa',
            'photo',
            'resume',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter student name'
            }),
            'register_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Register number'
            }),
            'department': forms.Select(attrs={
                'class': 'form-control'
            }),
            'cgpa': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Eg: 7.5'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'resume': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


# =========================
# COMPANY FORM  ✅ FIXED
# =========================
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'name',
            'location',
            'job_role',
            'department',
            'package',
            'min_cgpa'
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company Name'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company Location'
            }),
            'job_role': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Job Role'
            }),
            'department': forms.Select(attrs={
                'class': 'form-control'
            }),
            'package': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Eg: 4 LPA'
            }),
            'min_cgpa': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Eg: 6.5'
            }),
        }