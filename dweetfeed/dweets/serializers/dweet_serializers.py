from rest_framework import serializers

from dweetfeed.dweets.models import Dweet
from dweetfeed.dweets.models  import DweetRelation
from dweetfeed.dweets.models  import Comments

from userprofile.models import UserProfile

from .user_serializer import UserSerializer

class CommentSerializerForDweet(serializers.ModelSerializer):
    """
    serializer for Comments model spcific to Dweet
    """    

    commented_user = UserSerializer(read_only=True)    

    class Meta:
        model = Comments
        fields = ('id','commented_user','comment','commented_at')

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
        
        #user = self.context.get("request").user.username
        dweet = validated_data['dweet_text']

        user = self.context.get("request").user
        #user = UserProfile.objects.get(username=user).only('id')
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
        likes = obj.reactions.filter(reaction=1).cache()
        likes_count = likes.count()
        return likes_count

    def get_dislikes(self, obj):
        """
        Return total dislikes of Dweet
        """
        dislikes = obj.reactions.filter(reaction=0).cache()
        dislikes_count = dislikes.count()
        return dislikes_count

    def get_redweet(self, obj):
        """
        Return total redweets of Dweet
        """
        redweet = obj.dweetrelation_set.all().cache()
        redweet_count = redweet.count()
        return redweet_count-1