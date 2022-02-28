from django import forms
from ..models.requests import ReputationFeedback
from django.core.exceptions import ValidationError
from ..models.requests import FeedbackReviewRequest

# class review_feedback_form(forms.Form):
#     """A form for creating a reputation feedback review request.
#     Not using a model form, to access validation more explicitly.
#     """
#
#     feedback = forms.ModelChoiceField(queryset=ReputationFeedback.objects.filter(receiver=CURRENT USER))
#     description = forms.CharField(label='Description', widget=forms.Textarea, max_length=3500)
#     evidence = forms.FileInput()
#
#     def clean_feedback(self):
#         good_feedback = self.cleaned_data['feedback']
#         if good_feedback.receiver is not CURRENT USER:
#             raise ValidationError("Don't complain about other people's reputations.")
#
#         return good_feedback


