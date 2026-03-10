from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Student, Company, InterviewQuestion, InterviewResult
from .forms import StudentForm, CompanyForm
import random


# =====================
# UTILITY
# =====================

def normalize_department(dept):
    if not dept:
        return None

    dept = dept.upper().strip()

    dept_map = {
        "CS": "CS",
        "CSE": "CS",
        "COMPUTER SCIENCE": "CS",

        "MATH": "MATH",
        "MATHS": "MATH",
        "MATHEMATICS": "MATH",

        "PHY": "PHY",
        "PHYSICS": "PHY",

        "CHEM": "CHEM",
        "CHEMISTRY": "CHEM",

        "STAT": "STAT",
        "STATISTICS": "STAT",
    }

    return dept_map.get(dept)


# =====================
# HOME & DASHBOARD
# =====================

def home(request):
    return render(request, "placement/home.html")


def dashboard(request):
    return render(request, "placement/dashboard.html")


# =====================
# STUDENT SECTION
# =====================

def register_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()   # 🔥 DO NOT override department
            return redirect("view_students")
        else:
            print(form.errors)  # debug
    else:
        form = StudentForm()

    return render(request, "placement/student_register.html", {
        "form": form
    })


def view_students(request):
    students = Student.objects.all()
    return render(request, "placement/view_students.html", {"students": students})


def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect("view_students")


# =====================
# COMPANY SECTION
# =====================

def add_company(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)

        if form.is_valid():
            company = form.save(commit=False)

            normalized_dept = normalize_department(company.department)
            if not normalized_dept:
                return HttpResponse("Invalid department")

            company.department = normalized_dept
            company.save()

            return redirect("view_companies")
    else:
        form = CompanyForm()

    return render(request, "placement/add_company.html", {"form": form})


def view_companies(request):
    companies = Company.objects.all()
    return render(request, "placement/view_companies.html", {"companies": companies})


def edit_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if request.method == "POST":
        form = CompanyForm(request.POST, instance=company)

        if form.is_valid():
            company = form.save(commit=False)

            normalized_dept = normalize_department(company.department)
            if not normalized_dept:
                return HttpResponse("Invalid department")

            company.department = normalized_dept
            company.save()

            return redirect("view_companies")
    else:
        form = CompanyForm(instance=company)

    return render(request, "placement/edit_company.html", {"form": form})


def delete_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    company.delete()
    return redirect("view_companies")


# =====================
# ELIGIBLE COMPANIES
# =====================

def eligible_companies(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    companies = Company.objects.filter(
        department=student.department,
        min_cgpa__lte=student.cgpa
    )

    return render(request, "placement/eligible_companies.html", {
        "student": student,
        "companies": companies
    })


# =====================
# INTERVIEW HOME
# =====================

def interview_home(request):
    students = Student.objects.filter(is_interview_passed=False)
    return render(request, "placement/interview_home.html", {
        "students": students
    })


# =====================
# START INTERVIEW (✅ CORRECT & SAFE)
# =====================

def start_interview(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if InterviewResult.objects.filter(student=student).exists():
        return HttpResponse("Interview already completed")

    dept = student.department

    valid_departments = dict(Student._meta.get_field("department").choices)

    if dept not in valid_departments:
        return HttpResponse("Invalid department")

    # =====================
    # GET → SHOW QUESTIONS
    # =====================
    if request.method == "GET":
        questions = list(
            InterviewQuestion.objects.filter(department=dept)
        )

        if not questions:
            return HttpResponse("No questions available")

        random.shuffle(questions)
        questions = questions[:10]

        request.session["interview_qids"] = [q.id for q in questions]

        return render(request, "placement/interview_questions.html", {
            "questions": questions,
            "student": student,
            "department": valid_departments[dept],
        })

    # =====================
    # POST → EVALUATE
    # =====================
    qids = request.session.get("interview_qids")
    if not qids:
        return HttpResponse("Session expired")

    questions = InterviewQuestion.objects.filter(id__in=qids)

    score = 0
    review = []

    for q in questions:
        selected = request.POST.get(str(q.id))
        correct = str(q.correct_option)

        options = {
            "1": q.option1,
            "2": q.option2,
            "3": q.option3,
            "4": q.option4,
        }

        is_correct = selected == correct
        if is_correct:
            score += 1

        review.append({
            "question": q.question,
            "selected": options.get(selected, "Not Answered"),
            "correct": options.get(correct),
            "is_correct": is_correct,
        })

    passed = score >= len(questions) // 2

    InterviewResult.objects.create(
        student=student,
        score=score,
        passed=passed
    )

    student.is_interview_passed = passed
    student.save()

    request.session.pop("interview_qids", None)

    return render(request, "placement/interview_result.html", {
        "student": student,
        "score": score,
        "total_questions": len(questions),
        "passed": passed,
        "review": review,
    })