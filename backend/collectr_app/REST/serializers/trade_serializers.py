"""
This file contains all the serializer related to trade
"""
from rest_framework import serializers
from ...models.profile import Profile
from ...models.items import Item
from ...models.trades import TradeComments, Trade, TradeAttachment

class ProfileSerializer(serializers.ModelSerializer):
    """
    A serializer class for representing user profile
    """
    class Meta:
        """
        A Meta class for ProfileSerializer
        """
        model = Profile
        fields = ['id', 'email', 'username', 'about']

class BookmarkUserSerializer(serializers.ModelSerializer):
    """
    A serializer class for user bookmark user
    """
    class Meta:
        """
        A Meta class for BookmarkUserSerializer
        """
        model = Profile
        fields = ['id', 'username']

""" 
A serializer class for items in the trade 
"""
class TradeItemSerializer(serializers.ModelSerializer):
    """
    A serializer class for Trade Item
    """

    class Meta:
        """
        A Meta class for TradeItemSerializer
        """
        model = Item
        fields = [
                  'id', 'name', 'description',
                  'cover_image', 'release_date'
                 ]

""" 
A serializer class for comments in the trade 
"""
class TradeCommentSerializer(serializers.ModelSerializer):
    """
    A serializer class for TradeComment
    """

    class Meta:
        """
        A Meta class for TradeCommentSerializer
        """
        model = TradeComments
        fields = ['trade', 'username', 'email', 'comment', 'timestamp']


""" 
A serializer class for attachments in the trade 
"""
class TradeAttachmentSerializer(serializers.ModelSerializer):
    """
    A serializer class for TradeAttachment
    """
    class Meta:
        """
        A Meta class for TradeAttachment
        """
        model = TradeAttachment
        fields = ['attachment', 'trade_id']


""" 
A serializer class trade reading (receiving infomation)
"""
class TradeReadSerializer(serializers.ModelSerializer):
    """
    A serializer class for reading information from trade
    """
    creator = ProfileSerializer(read_only=True)
    have = TradeItemSerializer(many=True, read_only=True)
    want = TradeItemSerializer(many=True, read_only=True)
    comments = TradeCommentSerializer(many=True, read_only=True)
    attachments = TradeAttachmentSerializer(many=True, read_only=True)
    bookmarked = serializers.SerializerMethodField()

    def get_bookmarked(self, obj):
        """
        A method for getting bookmarked trade
        """
        request = self.context.get('request')

        if request is None:
            return False

        if request.user.id:
            # restore this when authentication works again!
            user = Profile.objects.get(id=request.user.id)
            trade = Trade.objects.get(id=obj.id)
            if user in trade.bookmarks.all():
                return True
            return False

        return False

    class Meta:
        """
        A Meta class for TradeReadSerializer
        """
        model = Trade
        fields = ['id', 'creator', 'description', 'active',
                  'creation_date', 'have', 'want', 'attachments', 'comments', 'bookmarked']


""" 
A serializer class for creating trade
"""

class TradeCreateSerializer(serializers.ModelSerializer):
    """
    A serializer class for creating trade
    """
    active = serializers.BooleanField(default=True)

    class Meta:
        """
        A Meta class for TradeCreateSerializer
        """
        model = Trade
        fields = ['id', 'creator', 'description', 'active', 'have', 'want']

# for user to add/remove themselves from the "bookmarks" list in a given trade
""" 
A serializer class for editing bookmark in the trade 
"""
class EditBookmarksSerializer(serializers.Serializer):
    """
    A serializer class for editing bookmarked trade
    """
    trade_id = serializers.CharField(read_only=True)

    class Meta:
        """
        A Meta class for EditBookmarkSerializer
        """
        fields = ['given_trade_id']
        extra_kwargs = {
            'trade_id': {'read_only': True},
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        """
        Method for validating trade
        """
        unchecked_id = self.initial_data['trade_id']
        trade = Trade.objects.get(id=unchecked_id)
        if trade is None:
            raise serializers.ValidationError({'bad_trade_id': 'Invalid trade ID.'})
        # else:
        #     if self.user in trade.bookmarks.all():
        #         raise serializers.ValidationError({
        #          'bookmarked': 'Already bookmarked, can\'t bookmark again.'
        #           })
        return unchecked_id


    def add_bookmark(self):
        """
        A method used for bookmarking trade
        """
        trade = Trade.objects.get(id=self.validated_data)
        profile = Profile.objects.get(username=self.user.username)
        trade.bookmarks.add(profile)
        print("\n You added a bookmark\n")
        return "the answer"


    def toggle_bookmark(self):
        """
        A method used for toggle bookmarked trades
        """
        trade = Trade.objects.get(id=self.validated_data)
        profile = Profile.objects.get(username=self.user.username)
        if self.user in trade.bookmarks.all():
            trade.bookmarks.remove(profile)
        else:
            trade.bookmarks.add(profile)
        return "the answer"
