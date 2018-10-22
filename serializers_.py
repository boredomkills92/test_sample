from rest_framework import serializers

from .models import Dweet
from .models import DweetRelation
from .models import Comments
from .models import Reaction

from userprofile.models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    """
    serializer for UserProfile model for Dweet relation
    """

    class Meta:
        model = UserProfile
        fields = ('id','username',)

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
    
class CommentSerializerForDweet(serializers.ModelSerializer):
    """
    serializer for Comments model spcific to Dweet
    """    

    commented_user = UserSerializer(read_only=True)    

    class Meta:
        model = Comments
        fields = ('id','commented_user','comment','commented_at')


class ReactionSerializer(serializers.Serializer):
    """
    serializer for Reaction
    """ 

    dweet_id = serializers.IntegerField()
    reaction = serializers.IntegerField()

class DweetRelationSerializer(serializers.ModelSerializer):
    """
    serializer for DweetRelation model from Dweet
    """ 

    user = UserSerializer(read_only=True)

    class Meta:
        model =DweetRelation
        fields = ('user','dweet_created_at','dweet_last_updated')

class DweetSerializer(serializers.ModelSerializer):
    """
    serializer for Dweet model
    """

    dweeted_user = UserSerializer(read_only=True, many=True)
    dweeted_relation = DweetRelationSerializer(source='dweetrelation_set',read_only=True, many=True)
    comments = CommentSerializerForDweet( many=True)
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()
    redweet = serializers.SerializerMethodField()
    
    #dweet_created_at = serializers.SerializerMethodField()
    #dweet_last_updated = serializers.SerializerMethodField()

    class Meta:
        model = Dweet
        fields = ('id','dweeted_user','dweeted_relation','dweet_text','comments','likes','dislikes','redweet')

    def create(self, validated_data):
        """
        Create Dweet for given dweet text
        """      

        user = self.context.get("request").user.username
        dweet = validated_data['dweet_text']

        user = UserProfile.objects.get(username=user)
        dweet = Dweet.objects.create( dweet_text = dweet)    
        dweetrelation = DweetRelation.objects.create(user = user , dweet = dweet)
        dweetrelation.save()

        return dweet

    def update(self, instance, validated_data):
        """
        Update comment for given Dweet
        """

        user = self.context.get("request").user
        comment_data = validated_data['comments'][0]['comment']
        instance.comments.create(comment=comment_data, commented_user=user)
        return instance

    def get_likes(self, obj):
        """
        Return total likes of Dweet
        """

        return obj.reactions.filter(reaction=1).count()

    def get_dislikes(self, obj):
        """
        Return total dislikes of Dweet
        """

        return obj.reactions.filter(reaction=0).count()

    def get_redweet(self, obj):
        """
        Return total redweets of Dweet
        """

        return obj.dweetrelation_set.all().count()-1

class ReDweetSerializer(serializers.Serializer):
    """
    serializer for ReDweeting
    """
    
    dweet_id = serializers.IntegerField()

