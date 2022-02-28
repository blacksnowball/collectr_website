from ..serializers.collection_serializers import *
from ..serializers.trade_serializers import *
from ..serializers.profile_serializers import *
from ...models import *
from drf_multiple_model.views import ObjectMultipleModelAPIView
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from rest_framework.response import Response
from rest_framework import pagination, status, generics, permissions
from ...REST import utils, collectr_throttles


class BasicPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class LimitPagination(MultipleModelLimitOffsetPagination):
    default_limit = 1000


"""
A user's profile, inc. multiple models: items, own trades, bookmarked trades, reputations.
"""
class ProfileAPIView(ObjectMultipleModelAPIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [collectr_throttles.Relaxed]

    pagination_class = LimitPagination

    def get_current_user(self):
        return Profile.objects.get(username=self.kwargs['username'])

    def get_querylist(self):
        me=self.get_current_user()

        querylist = [
            {
                'queryset': Profile.objects.filter(username=self.kwargs['username']),
                'serializer_class': ProfileSerializer,
                'label': 'profile',
            },
            {
                'queryset': utils.user_items_all(me),
                'serializer_class': ItemDetailSerializer,
                'label': 'my_items',
            },
            {
                'queryset': ReputationFeedback.objects.filter(receiver=me),
                'serializer_class': FeedbackReadSerializer,
                'label': 'reputations'
            },
            {
                'queryset': trades.Trade.objects.filter(creator=me),
                'serializer_class': TradeReadSerializer,
                'label': 'my_trades'
            },
            {
                'queryset': trades.Trade.objects.filter(bookmarks=me),
                'serializer_class': TradeReadSerializer,
                'label': 'bookmarked_trades'
            },
        ]
        return querylist


""" 
A view for providing another user feedback
"""
class GiveFeedbackView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [collectr_throttles.Relaxed]

    # strict throttle not needed as DB/serializer ensure sender+receiver unique together.
    # sender is current user
    # receiver is provided by url
    serializer_class = FeedbackWriteSerializer
    lookup_field = id

    def post(self, request, *args, **kwargs):
        current_user = self.request.user
        url_user = Profile.objects.get(id=self.kwargs['receiver_id'])
        serializer = self.serializer_class(data=request.data, sender=current_user, receiver=url_user)
        if serializer.is_valid(raise_exception=True):
            serializer.save(receiver=url_user, sender=current_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

