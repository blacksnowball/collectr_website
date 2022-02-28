"""
This file contains all the serializers related to request
"""
from rest_framework import serializers
from ...models.profile import Profile
from ...models.requests import NewItemRequest, NewCollectionRequest
class ProfileSerializer(serializers.ModelSerializer):
    """
    A serializer class for representing user profile
    """
    class Meta:
        """
        A Meta class for ProfileSerializer
        """
        model = Profile
        fields = [ 'id', 'username', 'email' ]

class NewItemRequestSerializer(serializers.ModelSerializer):
    """
    A serializer class for adding new item request
    """
    isActive = serializers.BooleanField(default=True)
    class Meta:
        """
        A Meta class for NewItemRequestSerializer
        """
        model = NewItemRequest
        fields = [
            'id', 'requester', 'new_name', 'description',
            'evidence', 'isActive', 'isApproved',
            'add_to_collection' 
        ]
class NewCollectionRequestSerializer(serializers.ModelSerializer):
    """
    A serializer class for adding nwe collection request
    """
    isActive = serializers.BooleanField(default=True)
    class Meta:
        """
        A serializer class for NewCollectionRequestSerializer
        """
        model = NewCollectionRequest
        fields = ['id', 'requester', 'description',
                  'evidence', 'new_name',
                  'isActive', 'isApproved'
                 ]
