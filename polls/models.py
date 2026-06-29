from django.db import models
from django.contrib.auth.models import User

class Poll(models.Model):
    
    question = models.CharField(max_length=255)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls')
    
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.question


class Choice(models.Model):
    
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    
    choice_text = models.CharField(max_length=255)
    
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.choice_text} (Sondaggio: {self.poll.question})"