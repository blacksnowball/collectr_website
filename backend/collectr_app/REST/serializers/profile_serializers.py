"""
This file contains all the serializers related to Profile
and feedback
"""
from rest_framework import serializers
from ... import models
class MiniProfileSerializer(serializers.ModelSerializer):
    """
    A class used to represent the user id and username
    """
    class Meta:
        """
        A Meta class to represent a miniature version of
        user profile
        """
        model = models.Profile
        fields = [ 'id', 'username',]


class FeedbackReadSerializer(serializers.ModelSerializer):
    """
    A serializer class for representing sender and receiver read
    communication
    """
    receiver = MiniProfileSerializer(many=False)
    sender = MiniProfileSerializer(many=False)
    class Meta:
        """
        A Meta class for Feedback Read Serializer
        """
        model = models.ReputationFeedback
        fields = ['id', 'receiver', 'sender', 'submission_type', 'comment', 'timestamp', 'flagged']


class FeedbackWriteSerializer(serializers.ModelSerializer):
    """
    A serializer class for representing sender and receiver write
    communication
    """
    def __init__(self, *args, **kwargs):
        self.sender = kwargs.pop('sender')
        self.receiver = kwargs.pop('receiver')
        super().__init__(*args, **kwargs)

    class Meta:
        """
        A Meta class for Feedback write serializer
        """
        model = models.ReputationFeedback
        fields = ['id', 'submission_type', 'comment',]


    def validate(self, attrs):
        """
        A method used to validate the sender and receiver
        """
    # this should be in the model, but...
        if self.sender==self.receiver:
            raise serializers.ValidationError('Kindly don\'t leave feedback on your own profile.')

        return super().validate(attrs)
