from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import Poll, Choice
from .serializers import PollSerializer


# --- LOGICA DEI SONDAGGI E DEI VOTI ---
class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def vote(self, request, pk=None):
        poll = self.get_object() 
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


# --- LOGICA DI REGISTRAZIONE UTENTI ---
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