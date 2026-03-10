from django.db import models

# =========================
# COMMON DEPARTMENT CHOICES
# =========================
DEPARTMENT_CHOICES = [
    ('CS', 'B.Sc Computer Science'),
    ('MATH', 'B.Sc Mathematics'),
    ('PHY', 'B.Sc Physics'),
    ('CHEM', 'B.Sc Chemistry'),
    ('STAT', 'B.Sc Statistics'),
]


# =========================
# STUDENT MODEL
# =========================
class Student(models.Model):
    name = models.CharField(max_length=100)
    register_no = models.CharField(max_length=20, unique=True)

    department = models.CharField(
        max_length=10,
        choices=DEPARTMENT_CHOICES
    )

    cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2
    )

    photo = models.ImageField(
        upload_to='students/photos/',
        blank=True,
        null=True
    )

    resume = models.FileField(
        upload_to='students/resumes/',
        blank=True,
        null=True
    )

    is_interview_passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.register_no})"


# =========================
# COMPANY MODEL
# =========================
class Company(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    job_role = models.CharField(max_length=200)

    department = models.CharField(
        max_length=10,
        choices=DEPARTMENT_CHOICES
    )

    package = models.CharField(max_length=50)  # Example: 4 LPA

    min_cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.name} - {self.job_role}"


# =========================
# INTERVIEW QUESTION MODEL
# =========================
class InterviewQuestion(models.Model):
    department = models.CharField(
        max_length=10,
        choices=DEPARTMENT_CHOICES
    )

    question = models.TextField()

    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)

    correct_option = models.IntegerField(
        choices=[
            (1, 'Option 1'),
            (2, 'Option 2'),
            (3, 'Option 3'),
            (4, 'Option 4'),
        ]
    )

    def __str__(self):
        return f"{self.get_department_display()} - {self.question[:40]}"


# =========================
# INTERVIEW RESULT MODEL
# =========================
class InterviewResult(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='interview_results'
    )

    department = models.CharField(
        max_length=10,
        choices=DEPARTMENT_CHOICES
    )

    score = models.IntegerField()
    total_questions = models.IntegerField(default=10)
    passed = models.BooleanField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'department')
        ordering = ['-created_at']

    def __str__(self):
        return (
            f"{self.student.name} | "
            f"{self.get_department_display()} | "
            f"Score: {self.score}/{self.total_questions}"
        )