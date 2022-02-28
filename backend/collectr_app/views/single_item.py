from django.http.response import HttpResponse
from django.shortcuts import render

from ..models.collections import *

from ..models import Item
from ..models import Collection
from ..models import Trade
from ..models.items import UserCollectsItem
import uuid

class ItemTraded(): 
    def __init__(self, trade, items): 
        self.trade = trade 
        self.items = items 
        self.user = Trade.objects.filter(id=trade.id)[0].creator

def has_collected(request):
    # username = name
    this_user = request.user
    return UserCollectsItem.objects.filter(user=this_user).count() > 0

def get_trades(item_name) -> list:
    trades = Trade.objects.filter(want=item_name)
    return trades

def format_item_name(item_name) -> list:
    items = item_name[1:len(item_name) -1].split(", ")
    for i in range(len(items)): 
        items[i] = items[i][1:len(items[i]) -1]
    return items 

def add_user_collection(user, collection):  
    UserCollection.objects.create(
        id=uuid.uuid4(),
        user=user,
        collection_id= collection
    )

def add_item_to_user(request):  
    item_name = ""
    item_id = ""
    if request.method == "POST": 
       item_name = request.POST['item'].split("|")[0]
       item_id = request.POST['item'].split("|")[1]
    
       item = Item.objects.get(id=item_id)
       count = 0
       for userCollection in UserCollection.objects.all():
           if userCollection.user == request.user and userCollection.id == item.collection:
               break 
           count += 1
       if count == UserCollection.objects.count(): 
         add_user_collection(request.user, item.collection)

           
    # Checking if the user already collected the item 
    collected = UserCollectsItem.objects.filter(user = request.user, id = item_id)
    
    if not collected:
        UserCollectsItem.objects.create(id = uuid.uuid4(), user = request.user, item_id = Item.objects.get(id=item_id))
    return display_a_single_item_page(request, item_name, item_id)

def get_traded_items(item_name) -> list:    
    trades = get_trades(item_name)
    traded_items = []
    for trade in trades: 
        items = format_item_name(trade.have)
        tmp_list = []
        for item in items: 
            tmp_list.append(Item.objects.filter(name=item)[0])
        traded_items.append(tmp_list)
    return traded_items 

def combine_trade_item(trades, items): 
    combinations = [] 
    for i in range(len(trades)):
        combinations.append(ItemTraded(trades[i], items[i]))
    return combinations


def display_a_single_item_page(request, name, item_id):

    item = Item.objects.get(id=item_id)
    collection_id = item.collection.collection_id
    collection = Collection.objects.filter(id=collection_id)[0]

    if has_collected(request):
        collected_text = u'\u2714' + " This item is in your collection"
    else:
        collected_text = u'\u2716' + " This item is not in your collection"

    item_name = f'["{item.name}"]'  
    traded_items = get_traded_items(item_name)
    
    contents = {
                "item": item,
                "collection": collection,
                "collected_text": collected_text, 
                "trades" : combine_trade_item(get_trades(item_name), traded_items)
                }
    return render(request, "items/single_item.html", contents)  

