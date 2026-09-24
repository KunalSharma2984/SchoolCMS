from django import forms
from .models import Course, Assignment, Submission


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('title', 'description', 'due_date', 'max_score')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('content', 'file')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your answer here...'}),
        }


class GradeForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('grade', 'feedback')
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_grade(self):
        grade = self.cleaned_data.get('grade')
        if grade is not None and grade > self.instance.assignment.max_score:
            raise forms.ValidationError(
                f'Grade cannot be higher than {self.instance.assignment.max_score}.'
            )
        return grade
