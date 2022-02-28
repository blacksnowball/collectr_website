'''
This file concerns defining the models related to Items in the Collectr application.
'''
import uuid
from collections import Collection
from profile import Profile
from django.db import models

class Item(models.Model):
    """
    Individual Item representation for a collection
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    collection = models.ForeignKey("Collection", related_name='items',
                                   on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=5000, blank=True)
    cover_image = models.ImageField(upload_to="uploads/", blank=True)
    release_date = models.DateField(auto_now=True, auto_now_add=False)
    cover_image = models.ImageField(upload_to="uploads/")

    def __str__(self):
        return f'{self.name}'


class UserCollectsItem(models.Model):
    """
    The table representation for determine whether or not a provided
    has collected an item from a collection
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("Profile", on_delete=models.CASCADE, null=False, blank=False)
    item_id = models.ForeignKey("Item", on_delete=models.CASCADE, null=False, blank=False)
