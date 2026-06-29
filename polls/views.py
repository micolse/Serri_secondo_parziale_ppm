from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import Poll, Choice
from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
   
    def has_object_permission(self, request, view, obj):
       
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.created_by == request.user
    
class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        poll = self.get_object()
        
        choices = poll.choices.all() 
        
        
        results_data = {
            "question": poll.question,
            "results": [
                {"text": choice.choice_text, "votes": choice.votes} 
                for choice in choices
            ]
        }
        return Response(results_data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated], serializer_class=VoteSerializer)
    def vote(self, request, pk=None):
        poll = self.get_object() 
        
        if not poll.is_active:
            return Response(
                {"error": "Questo sondaggio è chiuso."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        choice_id = request.data.get('choice_id') 

        if not choice_id:
            return Response(
                {"error": "Devi specificare il 'choice_id' per votare."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            choice = poll.choices.get(pk=choice_id)
        except Choice.DoesNotExist:
            return Response(
                {"error": "Questa opzione di risposta non esiste per questo sondaggio."}, 
                status=status.HTTP_404_NOT_FOUND
            )

        choice.votes += 1
        choice.save()

        return Response(
            {"message": f"Voto registrato con successo per: '{choice.choice_text}'!"}, 
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def toggle_status(self, request, pk=None):
        poll = self.get_object()
        
        if poll.created_by != request.user:
            return Response(
                {"error": "Non hai i permessi per modificare lo stato di questo sondaggio."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        poll.is_active = not poll.is_active
        poll.save()
        
        stato = "aperto" if poll.is_active else "chiuso"
        return Response(
            {"message": f"Il sondaggio è stato {stato} con successo", "is_active": poll.is_active},
            status=status.HTTP_200_OK
        )

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')

    if not username or not password:
        return Response(
            {"error": "Username e password sono obbligatori."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Questo username è già registrato."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(username=username, password=password, email=email)
    token = Token.objects.create(user=user)

    return Response(
        {
            "message": "Utente registrato con successo!",
            "token": token.key
        }, 
        status=status.HTTP_201_CREATED
    )
    
class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]