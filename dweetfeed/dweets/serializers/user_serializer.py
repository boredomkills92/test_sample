from rest_framework import serializers

from userprofile.models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    """
    serializer for UserProfile model for Dweet relation
    """

    class Meta:
        model = UserProfile
        fields = ('id','username',)