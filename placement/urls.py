from django.urls import path
from . import views

urlpatterns = [

    # =====================
    # HOME & DASHBOARD
    # =====================
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # =====================
    # STUDENT SECTION
    # =====================
    path('student/register/', views.register_student, name='register_student'),
    path('students/', views.view_students, name='view_students'),

    path(
        'student/delete/<int:student_id>/',
        views.delete_student,
        name='delete_student'
    ),

    path(
        'student/<int:student_id>/eligible-companies/',
        views.eligible_companies,
        name='eligible_companies'
    ),

    # =====================
    # COMPANY SECTION
    # =====================
    path('company/add/', views.add_company, name='add_company'),
    path('companies/', views.view_companies, name='view_companies'),

    path(
        'company/edit/<int:company_id>/',
        views.edit_company,
        name='edit_company'
    ),

    path(
        'company/delete/<int:company_id>/',
        views.delete_company,
        name='delete_company'
    ),

    # =====================
    # INTERVIEW SECTION
    # =====================
    path('interview/', views.interview_home, name='interview_home'),

    # ✅ FINAL & CORRECT
    path(
        'interview/start/<int:student_id>/',
        views.start_interview,
        name='start_interview'
    ),
]