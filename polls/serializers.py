from rest_framework import serializers
from .models import Poll, Choice

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'poll', 'choice_text', 'votes']
        read_only_fields = ['votes']  

class PollSerializer(serializers.ModelSerializer):
    
    choices = ChoiceSerializer(many=True, read_only=True)
    
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Poll
        fields = ['id', 'question', 'created_by', 'created_at', 'is_active','choices']
        
class VoteSerializer(serializers.Serializer):
    choice_id = serializers.IntegerField()