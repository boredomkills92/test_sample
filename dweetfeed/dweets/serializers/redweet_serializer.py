from rest_framework import serializers

class ReDweetSerializer(serializers.Serializer):
    """
    serializer for ReDweeting
    """
    
    dweet_id = serializers.IntegerField()