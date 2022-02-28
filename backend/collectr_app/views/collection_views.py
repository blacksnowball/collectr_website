from django.shortcuts import render
from django.http import HttpResponse
from ..models import Item
from ..models import Collection
from ..models import UserCollectsItem
from ..models.collections import UserCollection

from math import floor
from django.contrib.auth.decorators import login_required


@login_required()
def collections_page(request):
    all_collections = Collection.objects.order_by('title')
    content = {"all_collections": all_collections}
    return render(request, 'collections/collections_page.html', content)


def view_collection(request, user_id):
    return HttpResponse("You are viewing the personal collection page")


def my_collection_page(request):
    user_collections = Collection.objects.filter(user=request.user)
    all_collections = []
    for collection in user_collections:
        all_collections.append(Collection.objects.get(id=collection.id.id))
    content = {"my_collections": all_collections}
    return render(request, 'collections/my_collection.html', content)


def get_number_of_items_collected(user, collection) -> int:
    items = []
    for item in UserCollectsItem.objects.filter(user=user): 
        if Item.objects.get(id=item.id.id).collection == collection:
            items.append(item.id)
    return len(items)


def item_page(request, name):
    collection = Collection.objects.get(title=name)
    items = Item.objects.order_by("name").filter(collection=collection.id)
    item_collected = get_number_of_items_collected(request.user, collection)

    content = { 
               "items": items,
               "collection": collection,
               "total_item": len(items),
               "item_collected": item_collected,
               "percentage": str(floor(item_collected/len(items)*100))
               }
    return render(request, 'items/item_page.html', content)

