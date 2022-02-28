"""
This file is used to represent everything related
to the collections
"""
import uuid
from profile import Profile
from django.db import models

class Collection(models.Model):
    """
    Collection model for representing a master set of items.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150, blank=True)
    description = models.TextField(max_length=5000, blank=True)
    cover_image = models.ImageField(upload_to="uploads/", blank=True)
    thumbnail = models.ImageField(upload_to="uploads/", blank=True)

    def __str__(self) -> str:
        return f'{self.title} {self.id}'

class UserCollection(models.Model):
    """
    Depreciated Model, do not use
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey("Profile", on_delete=models.CASCADE)
    collection_id = models.ForeignKey("Collection", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user} for user: {self.id}'
