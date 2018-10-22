from rest_framework import serializers

from dweetfeed.dweets.models import Dweet
from dweetfeed.dweets.models import Comments

from .user_serializer import UserSerializer

class DweetSerializerForComment(serializers.ModelSerializer):
    """
    serializer for Dweet model specific to Comment Serialier
    """

    dweeted_user = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Dweet
        fields = ('id','dweeted_user','dweet_text',)


class CommentSerializer(serializers.ModelSerializer):
    """
    serializer for Comments model
    """    

    dweet_id = serializers.ReadOnlyField()
    commented_user = UserSerializer(read_only=True)
    dweet = DweetSerializerForComment(read_only=True)

    class Meta:
        model = Comments
        fields = ('id','dweet_id','commented_user','comment','dweet','commented_at')
        extra_kwargs = {'commented_at':{'read_only':True}}