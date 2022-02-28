from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from ..models import *
from datetime import datetime
import uuid
import json

def get_trades_and_screenshots_by_user(user, only_active_trades):

    if only_active_trades:
        get_trade_and_screenshots(Trade.objects.filter(creator=user, active=True))

    return get_trade_and_screenshots(Trade.objects.filter(creator=user))

def get_all_trades_and_screenshots(only_active_trades):

    if only_active_trades:
        return get_trade_and_screenshots(Trade.objects.filter(active=True).order_by('creation_date'))

    return get_trade_and_screenshots(Trade.objects.order_by('creation_date'))

def get_trade_and_screenshots(trades):

    all_have_items = []
    all_want_items = []

    for trade in trades:
        # supplied trades should be filtered already, but this is just temporary
        have_items = trade.have.all()
        want_items = trade.want.all()
        all_have_items.append(have_items)
        all_want_items.append(want_items)

    return zip(trades, all_have_items, all_want_items)

def index(request):
    '''
    Landing page that showcases the most recently posted trades.
    '''
    context = {'trades_and_screenshots': get_all_trades_and_screenshots(True)}
    return render(request, 'index.html', context)


def view_all_trades(request):
    """
    Called when viewing all trades on the landing page.
    """
    return HttpResponse("Viewing trades on the landing page.")


def search_trades(request):
    """
    Called when searching for trades.
    """

    if request.method == 'GET':
        collections = Collection.objects.order_by('title')
        items = Item.objects.order_by('collection')
        content = {'collections': collections, 'items': items}
        return render(request, 'search_trade_post.html', content)

    if request.method == 'POST':
        description = request.POST.get('description_searched')
        author = request.POST.get('author_searched')

        have_items = request.POST.getlist('have')
        want_items = request.POST.getlist('want')

        # have and want items rendered as objects
        have_items = [Item.objects.get(name=have_item) for have_item in have_items]
        want_items = [Item.objects.get(name=want_item) for want_item in want_items]

        matching_trades_want_item = Trade.objects.all().filter(description__contains=description,
                                                     creator__username__icontains=author, have__in=have_items, active=True)
        matching_trades_have_item = Trade.objects.all().filter(description__contains=description,
                                                     creator__username__icontains=author, want__in=want_items, active=True)

        matching_trades = matching_trades_have_item.union(matching_trades_want_item)

        return render(request, 'search_trade_post.html', {"matching_trades": get_trade_and_screenshots(matching_trades)})

    return render(request, 'search_trade_post.html')


def bookmark_post(request, trade_id):

    trade_post = Trade.objects.get(id=trade_id)

    if trade_post.bookmarks.filter(username=request.user.username):
        print("The user has bookmarked this trade! Unbookmarking it now...")
        trade_post.bookmarks.remove(Profile.objects.get(username=request.user.username))
    else:
        print("The user has not bookmarked this trade! Bookmarking it now...")
        trade_post.bookmarks.add(Profile.objects.get(username=request.user.username))

    return HttpResponseRedirect('/trades/{0}/'.format(trade_id))


def view_bookmarked_trades(request):
    bookmarked_trades = Trade.objects.filter(bookmarks=Profile.objects.get(username=request.user.username))
    return render(request, 'bookmarked_post.html', {"bookmarked_trades": get_trade_and_screenshots(bookmarked_trades)})


def create_trade_post(request):
    """
    Called when creating a new trade post.
    """
    if request.method == 'GET':
        collections = Collection.objects.order_by('title')
        items = Item.objects.order_by('collection')
        content = {'collections': collections, 'items': items}
        return render(request, 'create_trade_post.html', content)

    elif request.method == 'POST':

        have_items = request.POST.getlist('have')
        want_items = request.POST.getlist('want')
        have_items = [Item.objects.get(name=have_item).id for have_item in have_items]
        want_items = [Item.objects.get(name=want_item).id for want_item in want_items]


        trade = Trade(
            id=uuid.uuid4(),
            creator=Profile.objects.get(username=request.user.username),
            description=request.POST.get('description'),
            active=True,
            creation_date=datetime.now()
        )

        trade.save()

        trade.have.set(have_items)
        trade.want.set(want_items)

        attachments = request.FILES.getlist('attachments[]')

        for attachment in attachments:
            attachment_obj = TradeAttachment.objects.create(attachment=attachment, trade_id_id=trade.id)
            attachment_obj.save()
            trade.attachments.add(attachment_obj)

        trade.save()

        return HttpResponseRedirect('/trades/{0}/'.format(trade.id))

    return HttpResponseNotAllowed('{0} Not allowed'.format(request.method))

def close_trade_post(request, trade_id):
    trade_post = Trade.objects.get(id=trade_id)
    trade_post.active = False
    trade_post.save()
    return HttpResponseRedirect('/trades/{0}/'.format(trade_id))

def view_trade_post(request, trade_id):
    """
    Called when viewing a particular trade
    """

    trade = Trade.objects.get(id=trade_id)
    creator = trade.creator

    have_items = trade.have.all()
    want_items = trade.want.all()
    screenshots = TradeAttachment.objects.filter(trade_id_id=trade.id)


    bookmarked = False

    if trade.bookmarks.filter(username=request.user.username).exists():
        bookmarked = True

    if request.method == 'POST':

        commenter = Profile.objects.get(username=request.user.username)

        comment = TradeComments(
            trade_id=trade.id,
            username=commenter,
            email=commenter,
            comment=request.POST.get('comment'),
            timestamp=datetime.now())

        comment.save()

        trade.comments.add(comment)

    comments = trade.comments.all()


    return render(request, 'display_trade_post.html',
                  {'trade': trade, 'user': creator, 'have_items': have_items,
                   'want_items': want_items, 'bookmarked': bookmarked, 'screenshots':screenshots, 'comments':comments})


def submit_comment(request, trade_id):

    trade = Trade.objects.filter(id=trade_id)

    if request.method == 'POST':


        comment = TradeComments(
            trade_id=trade,
            user=Profile.objects.get(username=request.user.username),
            comment=request.POST.get('comment'),
            timestamp=datetime.now())

        comment.save()

        print(comment)

    return HttpResponseRedirect('/trades/{0}/'.format(trade_id))


def view_user_trades(request, username):
    """
    Called when viewing the history of trades of a user.
    """
    context = {'trades_and_screenshots': get_trades_and_screenshots_by_user(Profile.objects.get(username=username), True)}
    return render(request, 'display_user_trades.html', context)
