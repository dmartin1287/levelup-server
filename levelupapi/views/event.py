"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event
from levelupapi.models.game import Game
from levelupapi.models.gamer import Gamer


class EventView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:

            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """

        events = Event.objects.all()

        game_id = request.query_params.get('game', None)
        if game_id is not None:
            events = events.filter(game_id=game_id)

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["game"])

        event = Event.objects.create(
            description=request.data["description"],
            date=request.data["date"],
            time=request.data["time"],
            game=game,
            organizers=gamer
        )
        serializer = EventSerializer(event)
        return Response(serializer.data)


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date',
                    'time', 'organizers', 'attendees')
        depth = 1
