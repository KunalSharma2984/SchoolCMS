from django.db import models
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='taught_courses',
        limit_choices_to={'role': 'teacher'},
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def student_count(self):
        return self.enrollments.count()


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments',
        limit_choices_to={'role': 'student'},
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} → {self.course.title}"


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    max_score = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"{self.title} ({self.course.title})"


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submissions',
    )
    content = models.TextField(help_text="Write your answer or paste a link to your work.")
    file = models.FileField(upload_to='submissions/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.PositiveIntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)

    class Meta:
        unique_together = ('assignment', 'student')

    def __str__(self):
        return f"{self.student.username} – {self.assignment.title}"

    def letter_grade(self):
        if self.grade is None:
            return '—'
        pct = self.grade / self.assignment.max_score * 100
        if pct >= 90: return 'A'
        if pct >= 80: return 'B'
        if pct >= 70: return 'C'
        if pct >= 60: return 'D'
        return 'F'
