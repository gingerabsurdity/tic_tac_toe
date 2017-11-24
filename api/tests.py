from django.test import TestCase, Client
from .models import Game, Turn
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse

class ModelTestCase(TestCase):
    """This class defines the test suite for the game model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.game = Game()
        self.game.save()
        self.turn = Turn()
        self.turn.coordinate = 0
        self.turn.player = 'X'
        self.turn.game_id = self.game
        

    def test_model_can_create_a_game(self):
        """Test the game model can create a game."""
        old_count = Game.objects.count()
        new_game = Game()
        new_game.save()
        new_count = Game.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_create_a_turn(self):
        """Test the turn model can create a turn."""
        old_count = Turn.objects.count()
        self.turn.coordinate = 1
        self.turn.player = 'O'
        self.turn.game_id = self.game
        self.turn.save()
        new_count = Turn.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_move(self):
        """Test the move can correctly apply a turn to the game."""  
        game = Game()
        game.board_state = 'NNNNNNNNN' 
        player_symbol = 'O'
        position = 1
        old_count = Turn.objects.count()
        game.move(position, player_symbol)
        self.assertEqual(game.board_state, 'NONNNNNNN')
        new_count = Turn.objects.count()
        self.assertNotEqual(old_count, new_count)

        game.closed = True
        player_symbol = 'X'        
        with self.assertRaises(Exception):
            game.move(position, player_symbol)

        game.closed = False
        position = -1
        with self.assertRaises(Exception):
            game.move(position, player_symbol)

        position = 9
        with self.assertRaises(Exception):
            game.move(position, player_symbol)

        position = 1
        with self.assertRaises(Exception):
            game.move(position, player_symbol)

        game.board_state = 'NNNNNNNXX' 
        position = 6
        self.assertEqual(game.winner, None)
        self.assertEqual(game.closed, False)
        game.move(position, player_symbol)
        self.assertEqual(game.winner, player_symbol)
        self.assertEqual(game.closed, True)

        game = Game()
        game.board_state = 'OXOOXXXON' 
        position = 8
        player_symbol = 'O'
        game.move(position, player_symbol)
        self.assertEqual(game.winner, 'Toe')
        self.assertEqual(game.closed, True)


    def test_check_toe(self):
        """Test the check_toe can correctly define a toe of the game.""" 
        game = Game()
        game.board_state = 'OXOXOXOXO'
        self.assertEqual(game.check_toe(), True)
        game.board_state = 'NNONNNNNNX'
        self.assertEqual(game.check_toe(), False)

    def test_position_available(self):
        """Test the position_available can correctly define an empty position (with N symbol)."""
        game = Game()
        game.board_state = 'NXOXOXOXO'
        position = 1 
        self.assertEqual(game.position_available(position), False)
        position = 0
        self.assertEqual(game.position_available(position), True)

    def test_set_symbol(self):
        """Test the set_symbol can correctly set a symbol of a player to the board."""
        game = Game()
        game.board_state = 'NXOXOXOXO'
        position = 0 
        player_symbol = 'O'
        game.set_symbol(position, player_symbol)
        self.assertEqual(game.board_state, 'OXOXOXOXO')

    def test_check_victory(self):
        """Test the check_toe can correctly define a victory of the player.""" 
        game = Game()
        game.board_state = 'NXOXOXOXO' 
        player_symbol = 'O'
        self.assertEqual(game.check_victory(player_symbol), True)

        game.board_state = 'NXOXOXNXO' 
        self.assertEqual(game.check_victory(player_symbol), False)

        game.board_state = 'NOOXOXNOO'
        self.assertEqual(game.check_victory(player_symbol), True)

        game.board_state = 'NNNNNNNNN'
        self.assertEqual(game.check_victory(player_symbol), False)

        game.board_state = 'NNNNNNOOO'
        self.assertEqual(game.check_victory(player_symbol), True)

        game.board_state = 'NNNNNONOO'
        self.assertEqual(game.check_victory(player_symbol), False)

class ViewTestCase(TestCase):    

    def test_add_new_game(self):
        """Test the new_game can create a game."""  
        client = Client()      
        old_count = Game.objects.count()
        response = client.get('/newgame/')
        new_count = Game.objects.count()
        self.assertNotEqual(old_count, new_count)
        """Test the new_game set correct board_state."""        
        self.assertEqual(response.json()['board_state'], 'NNNNNNNNN')


    def test_make_turn(self):
        """Test the make_turn can apply valid turn to the board."""  
        client = Client() 
        game = Game()
        response = client.get('/newgame/')
        position = 6
        player_symbol = 'X'
        id = 1
        response = client.post('/maketurn/', {'id':id, 'position':position, 'player_symbol':player_symbol})
        self.assertEqual(response.json()['board_state'], 'NNNNNNXNN')

    def test_get_turns(self):
        """Test the get_turns return turns of the game.""" 
        client = Client() 
        game = Game()        
        response = client.get('/newgame/')
        old_response = client.get('/getturns/1')
        position = 6
        player_symbol = 'X'
        response = client.post('/maketurn/', {'id':1, 'position':position, 'player_symbol':player_symbol})
        new_response = client.get('/getturns/1')
        self.assertNotEqual(old_response, new_response)
