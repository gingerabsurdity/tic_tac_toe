from django.shortcuts import render

from rest_framework.views import APIView

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers
from django.http import JsonResponse
from rest_framework import generics, viewsets
from .serializers import GameSerializer, TurnSerializer
from .models import Game, Turn
from django.views import View
from django.shortcuts import get_object_or_404

@api_view(['GET'])	
def add_new_game(request):	
	new_game = Game()
	new_game.save()
	return Response({"id": new_game.id, "state": new_game.current_state})	

@api_view(['GET'])		
def get_turns(request, game_id):	
	turns = Turn.objects.all().filter(game_id = game_id)
	serializer = TurnSerializer(turns, many=True)
	return Response(serializer.data)

@api_view(['GET', 'POST'])
def make_turn(request):
	try:
		id = request.data.get('id')
		game = get_object_or_404(Game, id=id)
		game.save()
		player_symbol=request.data.get('player_symbol')
		position = int(request.data.get('position'))
		if (player_symbol == game.next_player_symbol) and (player_symbol in [Game.PLAYER1, Game.PLAYER2]):
			game.move(position, player_symbol)
			if game.winner:
				return Response({'current_state': 'closed', 'winner': game.winner})
			return Response({'current_state': game.current_state, 'next_player_symbol': game.next_player_symbol})
		else:
			return Response("Not your turn!")
	except Exception as e:
		return Response(str(e))