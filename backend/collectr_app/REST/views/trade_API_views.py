from datetime import date, datetime
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.utils import json
from ...REST import utils, collectr_throttles
from ..serializers.trade_serializers import *
from ...models import *
from rest_framework import generics,  permissions


"""
A view for listing all the trades related to the user
"""
class UserTradeList(ListCreateAPIView):
    """
    List all trades belonging to a given user.
    """
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [collectr_throttles.Relaxed]
    serializer_class = TradeReadSerializer
    lookup_url_kwarg = 'user_id'

    def post(self, request, *args, **kwargs):
        serializer = TradeCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        user = Profile.objects.get(id=user_id)
        trades = Trade.objects.filter(creator=user).order_by('-creation_date')
        return trades

""" 
A view for listing all the user bookmarked trades
"""
class UserBookmarkTradeList(ListAPIView):
    """
    List all trades belonging to a given user.
    """
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [collectr_throttles.Relaxed]
    serializer_class = TradeReadSerializer
    lookup_url_kwarg = 'user_id'

    def get_queryset(self):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        user = Profile.objects.get(id=user_id)
        bookmarked_trades = Trade.objects.filter(bookmarks=user).order_by('-creation_date')
        return bookmarked_trades

"""
A view for listing all the trade list in the landing page
"""
class TradeList(ListAPIView):
    """
    List all trades, or create a new trades.
    """
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [collectr_throttles.Relaxed]
    serializer_class = TradeReadSerializer

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            # Since the ReadSerializer does nested lookups
            # in multiple tables, only use it when necessary
            return TradeReadSerializer
        return TradeCreateSerializer

    def format_items(self, user_values):

        if ',' in user_values[0]:
            user_values = user_values[0].split(',')

        return [Item.objects.get(id=user_value) for user_value in user_values]

    def get_queryset(self):
        queryset = Trade.objects.all().order_by('-creation_date')
        queryset = queryset.filter(active=True)

        description = self.request.query_params.get('description')
        author = self.request.query_params.get('creator')
        have_items = self.request.query_params.getlist('have')
        want_items = self.request.query_params.getlist('want')

        # need a validation check that some items are here!

        have_queryset = None
        want_queryset = None
        union = False

        if have_items:
            have_items = self.format_items(have_items)
            have_queryset = Trade.objects.all().filter(have__in=have_items, active=True)

        if want_items:
            want_items = self.format_items(want_items)
            want_queryset = Trade.objects.all().filter(want__in=want_items, active=True)

        if have_items and want_items:
            queryset = have_queryset.union(want_queryset)
            union = True
        elif have_items and not want_items:
            queryset = have_queryset
        elif want_items and not have_items:
            queryset = want_queryset

        if description:
            queryset = queryset.filter(description__contains=description)

        if author:
            queryset = queryset.filter(creator__username__icontains=author)

        if union:
            return queryset

        return queryset.distinct()

""" 
A view for handling create trade
"""
class TradeListCreateView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [collectr_throttles.Strictest]
    serializer_class = TradeCreateSerializer
    queryset = Trade.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = TradeCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
A view for displaying individual trade in detail
"""
class IndividualTradeDetail(RetrieveUpdateAPIView):
    """
    Retrieve a single trade or update it.
    """
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [collectr_throttles.Relaxed]
    queryset = Trade.objects.all()
    serializer_class = TradeReadSerializer

"""
A view for displaying trade attachment in detail
"""
class TradeAttachmentsDetail(ListCreateAPIView):
    """
    Retrieve a single trade or update it.
    """
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [collectr_throttles.Relaxed]
    queryset = TradeAttachment.objects.all()
    serializer_class = TradeAttachmentSerializer

    lookup_url_kwarg = 'pk'

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        images = self.request.FILES
        pk = self.kwargs.get(self.lookup_url_kwarg)
        trade = Trade.objects.get(id=pk)
        for image in images.values():
            attachment = TradeAttachment.objects.create(attachment=image, trade_id=trade)
            trade.attachments.add(attachment)
        return HttpResponse(json.dumps({'message': "Uploaded"}), status=200)

    def get_queryset(self):
        pk = self.kwargs.get(self.lookup_url_kwarg)
        trade = Trade.objects.get(id=pk)
        return trade.attachments.all()


""" 
A view for displaying trade comment
"""
class TradeCommentDetail(ListCreateAPIView):
    """
    Retrieve a single trade or update it.
    """
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [collectr_throttles.Relaxed]
    serializer_class = TradeCommentSerializer
    lookup_url_kwarg = 'pk'

    def perform_create(self, serializer):
        pk = self.kwargs.get(self.lookup_url_kwarg)

        trade = Trade.objects.get(id=pk)


        username = self.request.data['username']
        username = Profile.objects.get(username=username)

        email = self.request.data['email']
        email = Profile.objects.get(email=email)

        comment = self.request.data['comment']


        new_comment = TradeComments(
            trade=trade,
            username=username,
            email=email,
            comment=comment,
            timestamp=datetime.now()
        )

        new_comment.save()

        trade.comments.add(new_comment)

    def get_queryset(self):
        pk = self.kwargs.get(self.lookup_url_kwarg)
        comments = TradeComments.objects.filter(trade=pk)
        return comments


""" 
A trade for editing book mark of a trade
"""
class EditBookmarksView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [collectr_throttles.Relaxed]
    serializer_class = EditBookmarksSerializer

    def post(self, request, *args, **kwargs):
        url_data = {'trade_id': self.kwargs['trade_id']}
        serializer = self.get_serializer(data=url_data, user=self.request.user)
        
        if serializer.is_valid(raise_exception=True):
            serializer.toggle_bookmark()

        return Response({'message': 'Success'}, status=status.HTTP_200_OK)

