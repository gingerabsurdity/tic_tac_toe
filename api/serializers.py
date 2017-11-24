from rest_framework import serializers
from .models import Game, Turn

class TurnSerializer(serializers.ModelSerializer):
	class Meta:
		model = Turn
		fields = ('id','game_id','player', 'coordinate')

class GameSerializer(serializers.ModelSerializer):
	class Meta:
		model = Game
		fields = ('id','player_name', 'coordinate')
		read_only_fields = ('winner','date_created','current_state')