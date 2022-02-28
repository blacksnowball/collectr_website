from ...models.requests import *
from ...models.collections import Collection
from ..serializers.collection_serializers import *
from ..serializers.requests_serializers import *
from ...REST import utils, collectr_throttles
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics,  permissions


# Creating a request for adding new collection
class AddNewCollectionRequest(generics.ListCreateAPIView): 
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [collectr_throttles.Stricter]
    serializer_class = NewCollectionRequestSerializer 
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        content = NewCollectionRequest.objects.all()
        return content
    
# Creating a request for adding new item
class AddNewItemRequest(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [collectr_throttles.Stricter]
    serializer_class = NewItemRequestSerializer 
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self): 
        content = NewItemRequest.objects.all()
        return content
    

# When the curator modified the request
class CollectionRequestManager(generics.ListCreateAPIView):
    permission_classes = [utils.IsCurator]
    throttle_classes = [collectr_throttles.Relaxed]
    serializer_class = NewCollectionRequestSerializer
    lookup_field = "id"
    
    def get_queryset(self): 
        new_collection_request = NewCollectionRequest.objects.filter(id=self.kwargs['id'])
        return new_collection_request
    
    def perform_create(self, serializer):  
        collection_request = NewCollectionRequest.objects.get(id=self.kwargs['id'])
        is_approved = self.request.data['isApproved'].lower() == 'true'
        collection_request.new_name=self.request.data['new_name']
        collection_request.isApproved=is_approved
        collection_request.isActive=False
        collection_request.save()
        
        if is_approved:
            new_collection = Collection(
                id=uuid.uuid4(), 
                title= collection_request.new_name,
                description= collection_request.description,
            )
            new_collection.save()

        collection_request.delete()
     
    
class ItemRequestManager(generics.ListCreateAPIView):
    permission_classes = [utils.IsCurator]
    throttle_classes = [collectr_throttles.Relaxed]
    serializer_class = NewItemRequestSerializer
    lookup_field = 'id'

    def get_queryset(self): 
        new_item_request = NewItemRequest.objects.filter(id=self.kwargs['id'])
        return new_item_request
    
    def perform_create(self, serializer): 
        new_item_request = NewItemRequest.objects.get(id=self.kwargs['id']) 
        is_approved = self.request.data['isApproved'].lower() == 'true'
        new_item_request.new_name = self.request.data['new_name']
        new_item_request.isApproved = is_approved
        new_item_request.isActive = False
        new_item_request.save()
        
        if is_approved:
            item_collection = Collection.objects.get(id=new_item_request.add_to_collection.id)
            new_item = Item (
                id=uuid.uuid4(),
                collection=item_collection,
                name=new_item_request.new_name,
                description=new_item_request.description, 
            )
            new_item.save()
        
        new_item_request.delete()
