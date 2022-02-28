"""
This file contains all the serializers for collection
"""
from rest_framework import serializers
from ...models.profile import Profile
from ...models.items import Item, UserCollectsItem
from ...models.collections import Collection
from ... REST import utils
class ProfileSerializer(serializers.ModelSerializer):
    """
    A serializer class for User model of the system
    """
    class Meta:
        """
        A Meta class for Profile Serializer
        """
        model = Profile
        fields = ['id', 'email', 'username', 'about']


class ItemDetailSerializer(serializers.ModelSerializer):
    """
    A serializer class for Item model of the system
    """
    collected = serializers.SerializerMethodField()

    def get_collected(self, obj):
        """
        A method used to determined whether or not
        the user has collected the item
        """
        item_id = obj.id
        user = self.context['request'].user.id
        for item in UserCollectsItem.objects.all():
            if item.item_id.id == item_id and user == item.user.id:
                return True
        return False

    class Meta:
        """
        A Meta class for Item Detail Serializer
        """
        model = Item
        fields = ['id', 'collection', 'name',
                'description', 'release_date', 'cover_image',
                'collected']


class CollectionSerializer(serializers.ModelSerializer):
    """
    A serializer class for Collection model of the system
    """
    item_count = serializers.SerializerMethodField()

    def get_item_count(self, obj):
        """
        A method used to get the number of items in a collection
        """
        return obj.items.count()

    class Meta:
        """
        A Meta class for Collection Serializer
        """
        model = Collection
        fields = [
            'id', 'title', 'item_count', 'description',
            'cover_image', 'thumbnail'
        ]


class AddCollectionSerializer(serializers.ModelSerializer):
    """
    A serializer class for Adding Collection
    """
    class Meta:
        """
        A Meta class for Add Collection Serializer
        """
        model = Collection
        fields = [ 'id', 'title', 'description', 'cover_image']


class UserCollectsItemSerializer(serializers.ModelSerializer):
    """
    A serializer class for representing collected item from a user
    """
    collected_count = serializers.SerializerMethodField()

    def get_collected_count(self, obj):
        """
        a method used to get the total collected items count
        """
        return utils.user_items_all(user=obj.user).count()

    class Meta:
        """
        A Meta class for User Collects Item Serializer
        """
        model = UserCollectsItem
        fields = ['id', 'user', 'item_id', 'collected_count']
