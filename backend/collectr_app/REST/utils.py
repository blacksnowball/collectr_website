"""
This file contains all the utility functions
used throughout the program
"""
from rest_framework.permissions import BasePermission
from ..models.items import UserCollectsItem, Item
from ..models.collections import Collection
#from serializers.collection_serializers import *

def user_items_all(user):
    """
    A function used to find all the items
    owned by a user
    """
    user_collects_items = UserCollectsItem.objects.filter(user=user)
    my_item_ids = []
    for user_collects_item in user_collects_items:
        my_item_ids.append(user_collects_item.item_id.id)

    return Item.objects.filter(id__in=my_item_ids)

def user_items_in_collection(user, collection):
    """
    A function used to find all the items related to a
    collection that has been collected by a user
    """
    user_collects_items = UserCollectsItem.objects.filter(user=user
                                                          ).filter(item_id__collection=collection)
    my_item_ids = []
    for user_collects_item in user_collects_items:
        my_item_ids.append(user_collects_item.item_id.id)

    return Item.objects.filter(id__in=my_item_ids)

def user_collections(user):
    """
    A function used to find all the collections owned by
    a user
    """
    user_collects_items = UserCollectsItem.objects.filter(user=user)
    my_collection_ids = []
    for user_collects_item in user_collects_items:
        my_collection_ids.append(user_collects_item.item_id.collection.id)

    return Collection.objects.filter(id__in=my_collection_ids)

def user_item_status(user, item):
    """
    A function used to determine whether or not
    a user has collected the item
    """
    user_collects_items = UserCollectsItem.objects.filter(user=user
                                                          ).filter(item_id=item)
    return (user_collects_items.count()!=0)

def printf(value):
    """
    A function use for print testing
    """
    print("="*20 + "\n" *3)
    print(value)
    print("\n" *3 + "=" * 20)

class IsCurator(BasePermission):
    """
    A class for representing curator
    """

    def has_permission(self, request, view):
        return request.user.is_staff
