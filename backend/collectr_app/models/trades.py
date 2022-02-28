"""
This file contains all information related to trade
"""
import uuid
from profile import Profile
from django.db import models
from .items import Item

class Trade(models.Model):
    '''
    A class used to represent the trade between 2 users
    '''
    # note that ids are automatically handled by django
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey("Profile", on_delete=models.CASCADE, null=False, blank=False)
    description = models.TextField(max_length=3500)
    active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    have = models.ManyToManyField("Item", null=False, blank=False, related_name="have_items")
    want = models.ManyToManyField("Item", null=False, blank=False, related_name="want_items")
    attachments = models.ManyToManyField("TradeAttachment")
    bookmarks = models.ManyToManyField("Profile", blank=True, related_name="bookmarks")
    comments = models.ManyToManyField("TradeComments", blank=True, related_name="trade_comments")

    def __str__(self) -> str:
        return f'{self.creator},  have: {self.have},  want: {self.want}'

class TradeAttachment(models.Model):
    """
    A class used to represent the attachment components of trade
    """
    attachment = models.FileField(upload_to="attachments/")
    trade_id = models.ForeignKey("Trade", on_delete=models.CASCADE, null=False, blank=False)

class TradeComments(models.Model):
    """
    A class used to represent the comment component of trade
    """

    # note that ids are automatically handled by django
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE,
                              null=False, blank=False,
                              related_name='comment_trade')
    username = models.ForeignKey("Profile", on_delete=models.CASCADE,
                                 null=False, blank=False,
                                 to_field='username', db_column='username',
                                 related_name='comment_username')
    email = models.ForeignKey("Profile", on_delete=models.CASCADE,
                              null=False, blank=False, to_field='email',
                              db_column='email', related_name='comment_email')
    comment = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

class ItemIsTraded(models.Model):
    """
    A class used to represent whether or not an item is traded
    """
    # note that in the ERD, this should be a composite PK but Django does not support this
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trade_id = models.ForeignKey(Trade, on_delete=models.CASCADE, null=False, blank=False)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE, null=False, blank=False)
    offered = models.BooleanField(default=True)
