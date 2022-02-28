from django.shortcuts import render
from math import floor

from ..models import *

from ..models import Item
from ..models import Collection

def get_collection(collection_name): 
    return Collection.objects.get(title=collection_name)

def get_items(user, collection) -> list: 
    items = []
    for item in UserCollectsItem.objects.filter(user=user): 
        if Item.objects.get(id=item.id.id).collection == collection:
            items.append(item.id)
    return items

def get_total_item(collection) -> int: 
    return len(Item.objects.order_by("name").filter(collection=collection.id))

def get_item_collected(user):
    this_user = user 
    # Now we need to look through the UserCollectsItem to find a list of items
    if UserCollectsItem.objects.count() == 0: 
        return 0 
    items = UserCollectsItem.objects.filter(user=this_user)

    # We now have a list of item id
    return items.count()
        
    
def view_my_items(request, collection_name):
    collection = get_collection(collection_name)
    items = get_items(request.user, collection)
    contents = { 
        'collection' : collection,
        'items' : items,
        'total_item' : get_total_item(collection),
        'item_collected': len(items),
        'percentage' : str(floor(len(items)/get_total_item(collection)*100))
    }
    return render(request, "items/my_item_page.html", contents)