from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from .forms import GradeForm
from .models import Assignment, Course, Enrollment, Submission


class CourseWorkflowTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username='teacher', password='test-password', role='teacher'
        )
        self.student = User.objects.create_user(
            username='student', password='test-password', role='student'
        )
        self.course = Course.objects.create(title='History', teacher=self.teacher)

    def test_enrollment_requires_post(self):
        self.client.force_login(self.student)

        get_response = self.client.get(reverse('enroll', args=[self.course.pk]))
        self.assertEqual(get_response.status_code, 405)
        self.assertFalse(Enrollment.objects.exists())

        post_response = self.client.post(reverse('enroll', args=[self.course.pk]))
        self.assertRedirects(
            post_response, reverse('course_detail', args=[self.course.pk])
        )
        self.assertTrue(
            Enrollment.objects.filter(student=self.student, course=self.course).exists()
        )

    def test_grade_cannot_exceed_assignment_maximum(self):
        assignment = Assignment.objects.create(
            course=self.course, title='Essay', max_score=20
        )
        submission = Submission.objects.create(
            assignment=assignment, student=self.student, content='My answer'
        )

        form = GradeForm({'grade': 21, 'feedback': ''}, instance=submission)

        self.assertFalse(form.is_valid())
        self.assertIn('higher than 20', form.errors['grade'][0])
