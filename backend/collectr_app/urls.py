from django.urls import path

from .REST.views.requests_API_views import CollectionRequestManager
from .views.my_item import *
from .views.trades_views import *
from .views.collection_views import *
from .views.single_item import *
from .views.whole_profile import *
from .views.request_views import *
from .REST.views.profile_API_views import *
from .REST.views.collections_API_views import *
from .REST.views.trade_API_views import *
from .REST.views.requests_API_views import * 



api_patterns = [ 
    # API trades
    path('api/trades/', TradeList.as_view(), name='api-all-trades'), # all trades
    path('api/trades/create/', TradeListCreateView.as_view(), name='api-create-trade'), # all trades
    path('api/trades/<pk>/', IndividualTradeDetail.as_view(), name='api-one-trade'), # specific trade
    path('api/trades/<pk>/comments/', TradeCommentDetail.as_view(), name='api-one-trade-comments'), # specific trade
    path('api/trades/<pk>/attachments/', TradeAttachmentsDetail.as_view(), name='api-one-trade-attachments'), # specific trade
    path('api/<uuid:user_id>/trades/', UserTradeList.as_view(), name='api-user-trades'), # trades of a user
    path('api/<uuid:user_id>/bookmarked/', UserBookmarkTradeList.as_view(), name='api-user-bookmarks'), # bookmarked trades of a user
    path('api/trades/<str:trade_id>/edit_bookmark/', EditBookmarksView.as_view(), name='api-bookmark-toggle'), #user can add/remove own bookmarks

    # API collections/items view-only urls:
    path('api/collections/', CollectionList.as_view(), name='all collections'),
    path('api/collections/mine/', MyCollectionList.as_view(), name='all my collections'),
    path('api/collections/<uuid:collection_id>/', SingleCollection.as_view(), name='single collection'),
    path('api/collections/<uuid:collection_id>/mine/', MySingleCollection.as_view(), name='my single collection'),
    path('api/item/<uuid:item_id>/', ItemDetailView.as_view(), name='item detail'),
    path('api/all_my_items/', AllMyItems.as_view(), name='my single collection'),

    #API collections/items editing:
    path('api/collect/<uuid:user_id>/<uuid:item_id>/', EditMyItemsView.as_view(), name='collect more'),
    path('api/new_item/', AddItemView.as_view()),
    path('api/new_collection/', AddCollectionView.as_view()),
    path('api/request/<uuid:id>/', CollectionRequestManager.as_view(), name="testing"),

    # API for request: 
    path('api/request/collection/', AddNewCollectionRequest.as_view(), name="add new collection request"),
    path('api/request/item/', AddNewItemRequest.as_view(), name="Add new Item Request"),
    path('api/request/collection/<uuid:id>/', CollectionRequestManager.as_view(), name="Approved Collection for new Collection"),
    path('api/request/item/<uuid:id>/', ItemRequestManager.as_view(), name="Approved Request for new Item"),

    #viewing all profile info:
    path('api/profile/<str:username>/', ProfileAPIView.as_view(), name='any-profile'),
    path('api/feedback/<uuid:receiver_id>/', GiveFeedbackView.as_view(), name='give-feedback'),

    #backup pattern, to catch incorrect urls..:
#    path('*', WrongURLView.asView(),)
]

urlpatterns = [
    path('', index, name='index'),
] + api_patterns

unused_patterns = [
    # non-API pages:
    path('profile/', whole_profile, name='profile'),

    path('collections/', collections_page, name="collection_page"),
    path('collections/my_collections/', my_collection_page, name="my collection"),
    # url(r'collections/', collections_page, name='collection_page')
    path('collections/<name>/items/', item_page, name="item page"),
    path('collections/<name>/items/<item_id>/',  display_a_single_item_page, name="single item"),
    path('collections/<collection_name>/my_items/', view_my_items, name="my-item"),
    path('add_item', add_item_to_user, name="add_item"),

    path('collections/new_collection/', newCollection.as_view(), name='new_collection'),
    path('collections/new_item/', newItem.as_view(), name='new_item'),

    path('trades/trade_home/', view_all_trades, name='all-trades'),
    path('trades/search/', search_trades, name='search-trades'),
    # url(r'^trades/search/', search_trades, name='search-trades'),
    path('trades/create/', create_trade_post, name='create-trade-post'),
    # path('<str:username>/trades/', view_user_trades, name='user-trades'),
    path('trades/<uuid:trade_id>/', view_trade_post, name='trade-post'),
    path('trades/<uuid:trade_id>/close/', close_trade_post, name='trade-post'),
    path('trades/bookmarked/', view_bookmarked_trades, name='view-bookmarked-trades'),
    path('trades/<uuid:trade_id>/bookmarked/', bookmark_post, name='bookmarked-trades'),
    path('collections/<collection_name>/my_items/', view_my_items, name="my-item"),
    path('add_item', add_item_to_user, name="add_item"),
    
]


