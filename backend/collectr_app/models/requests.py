"""
This file contains everything related to request,
"""
import uuid
import datetime
from profile import *
from collections import Collection
from django.db.models import UniqueConstraint
from django.db import models
class Request(models.Model):
    '''
    Request base class & main 3 x request types: reputation feedback review,
    new collection & new item.
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requester = models.ForeignKey("Profile", on_delete=models.CASCADE, null=False, blank=False)
    new_name = models.CharField(max_length=150, blank=True)
    description = models.TextField(max_length=5000)
    evidence = models.TextField(max_length=5000)
    isActive = models.BooleanField(default=True)
    isApproved = models.BooleanField(default=False)

    class Meta:
        """A Meta class for Request Model"""
        abstract = True
class FeedbackReviewRequest(Request):
    """
    Feedback Request class that inherits from request, with an addition
    of feedback attribute added to it to represent another user feedback
    """
    feedback = models.ForeignKey("ReputationFeedback", editable=False, on_delete=models.CASCADE)

    def __str__(self):
        return f'Disputing feedback from {self.feedback}'

    @property
    def receiver(self):
        """
        A method for processing another user feedback
        """
        return self.feedback.receiver

    class Meta:
        """
        A Meta class for Feedback Review Request
        """
        constraints = [
            UniqueConstraint(name='one dispute per feedback',
                             fields=['feedback']
                             ),
        ]

class NewCollectionRequest(Request):
    """
    A class for representing new request to add new collection
    to the database
    """

    def __str__(self):
        return f'Add collection: {self.new_name}'

class NewItemRequest(Request):
    """
    A class for representing new request to add new item of a
    collection to the database
    """
    add_to_collection = models.ForeignKey("Collection", on_delete=models.CASCADE)

    def __str__(self):
        return f'Add item: {self.new_name} to {self.add_to_collection}'
