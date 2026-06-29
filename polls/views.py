from rest_framework import viewsets, permissions
from .models import Poll, Choice
from .serializers import PollSerializer

class PollViewSet(viewsets.ModelViewSet):
    
    queryset = Poll.objects.all()
    
    serializer_serializer = PollSerializer
    serializer_class = PollSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)