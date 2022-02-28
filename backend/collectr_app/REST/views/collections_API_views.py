from rest_framework import generics
from ..serializers.collection_serializers import *
from rest_framework.response import Response
from rest_framework import generics, status, views, permissions
from drf_multiple_model.views import ObjectMultipleModelAPIView
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination

from rest_framework import pagination
from ...REST import utils, collectr_throttles

""" 
Django pagination option to allow for multiple models
"""
class BasicPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10

class LimitPagination(MultipleModelLimitOffsetPagination):
    default_limit = 1000

"""
A view for displaying a list of collection
"""
class CollectionList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [collectr_throttles.Relaxed]

    serializer_class = CollectionSerializer 
    queryset = Collection.objects.all().order_by("title")


"""
A view for showing personal collection 
"""
class MyCollectionList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [collectr_throttles.Relaxed]
    serializer_class = CollectionSerializer 

    def get_queryset(self): 
        user = self.request.user.id
        return utils.user_collections(user)


"""
A view for showing a single collection
"""
class SingleCollection(ObjectMultipleModelAPIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [collectr_throttles.Relaxed]
    serializer_class = ItemDetailSerializer
    lookup_url_kwarg = 'collection_id'
    pagination_class = LimitPagination

    def get_querylist(self):
        items = Item.objects.order_by("name").filter(collection=self.kwargs['collection_id'])

        #collection = Collection.objects.filter(id=items[0].collection.id)
        collection = Collection.objects.filter(id=self.kwargs['collection_id'])
        context = {'user': self.request.user}

        if (len(items) == 0):
            querylist = [
                {
                    'queryset': collection,
                    'serializer_class': CollectionSerializer,
                }
            ]
        else:
            querylist = [
                {
                    'queryset': items,
                    'serializer_class': ItemDetailSerializer,
                    'serializer': ItemDetailSerializer(context),
                },
                {
                    'queryset' : collection,
                    'serializer_class': CollectionSerializer,
                }
            ]
        return querylist

"""
A view for showing a single collection for a user
"""
class MySingleCollection(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [collectr_throttles.Relaxed]
    serializer_class = ItemDetailSerializer

    def get_queryset(self):
        return utils.user_items_in_collection(user=self.request.user, collection=self.kwargs['collection_id'])


"""
A view for showing detail information about item
"""
class ItemDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [collectr_throttles.Relaxed]
    serializer_class = ItemDetailSerializer
    lookup_url_kwarg = 'item_id'

    def get_queryset(self):
        return Item.objects.order_by("name").filter(id=self.kwargs['item_id'])
    
"""
A view for showing all items related to a user
"""
class AllMyItems(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [collectr_throttles.Relaxed]
    serializer_class = ItemDetailSerializer

    def get_queryset(self):
        return utils.user_items_all(self.request.user.id)


#CRUD views:
""" 
A view for editing user item
"""
class EditMyItemsView(generics.ListCreateAPIView, generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [collectr_throttles.Relaxed]
    serializer_class = UserCollectsItemSerializer
    lookup_field = 'item_id'

    # Get request
    def get_queryset(self):
        user=self.request.user.id
        return UserCollectsItem.objects.filter(user=user)


""" 
A view for adding user item
"""

class AddItemView(generics.CreateAPIView):
    permission_classes = [utils.IsCurator]
    throttle_classes = [collectr_throttles.Medium]
    serializer_class = ItemDetailSerializer

    def get_queryset(self):
        return Item.objects.filter(id=self.kwargs['item_id'])

"""
A view for addding a collection
"""
class AddCollectionView(generics.CreateAPIView):
    permission_classes = [utils.IsCurator]
    throttle_classes = [collectr_throttles.Medium]
    serializer_class = AddCollectionSerializer
    queryset = Collection.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = AddCollectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

