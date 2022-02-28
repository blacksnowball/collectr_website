from django.shortcuts import render
from ..models import *


def whole_profile(request):
    """
    Displays user's info in bulk: profile/items/trades/reputations/bookmarks
    """
    currentUser = request.user
    #currentUser = Profile.objects.get(username=request.user)

    #Collected Items
    my_item_ids = UserCollectsItem.objects.filter(user=currentUser)
    my_items = []
    for my_item_id in my_item_ids:
        my_items.append(Item.objects.get(id=my_item_id.id.id))

    #Reputations


    #Own Trades
    own_trades = list(Trade.objects.filter(creator=currentUser))

    #Bookmarked Trades
    bookmarked_trades = list(Trade.objects.filter(bookmarks=Profile.objects.get(username=currentUser.username)))

    context = {"user": currentUser,
               "items": my_items,
               "own_trades": own_trades,
               "bookmarked_trades": bookmarked_trades,
               }
    return render(request, 'whole_profile.html', context)

