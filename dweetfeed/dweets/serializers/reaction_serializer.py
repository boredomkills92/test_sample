from rest_framework import serializers

class ReactionSerializer(serializers.Serializer):
    """
    serializer for Reaction
    """ 

    dweet_id = serializers.IntegerField()
    reaction = serializers.IntegerField()