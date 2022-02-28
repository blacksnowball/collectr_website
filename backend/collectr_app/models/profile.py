"""
This file is used to represent everything related
to the users
"""
import uuid
from django.contrib import auth
from django.db import models
from django.db.models import UniqueConstraint

class Profile(auth.get_user_model()):
    """
    A profile class used to model the user
    """
    class Meta:
        """A Meta class for this model"""
        proxy = True

class ReputationFeedback(models.Model):
    """
    A reputation class used to model the feedback related to a particular
    user reputation
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    receiver = models.ForeignKey("Profile", related_name='receiver',
                                on_delete=models.CASCADE, null=False, blank=False)
    sender = models.ForeignKey("Profile", related_name='sender',
                               on_delete=models.CASCADE, null=False, blank=False)
    submission_type = models.BooleanField(default=False, blank=False)
    comment = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    flagged = models.BooleanField(default=False)

    class Meta:
        """A Meta class for this model"""
        constraints = [
            UniqueConstraint(name='rate-limiting-feedbacks',
                             fields=['receiver', 'sender']
                             ),
        ]
