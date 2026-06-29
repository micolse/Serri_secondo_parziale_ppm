from rest_framework import serializers
from .models import Poll, Choice

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'votes']

class PollSerializer(serializers.ModelSerializer):
    
    choices = ChoiceSerializer(many=True, read_only=True)
    
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Poll
        fields = ['id', 'question', 'created_by', 'created_at', 'choices']