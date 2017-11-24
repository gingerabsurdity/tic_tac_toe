from django.db import models

class Turn(models.Model):
	player = models.CharField(max_length=255, blank=True)
	coordinate = models.IntegerField(null=True)
	game_id = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE,
    )



class Game(models.Model):
	
	PLAYER1 = 'X'
	PLAYER2 = 'O'

	current_state = models.CharField(max_length=255, blank=False, default="NNNNNNNNN")
	date_created = models.DateTimeField(auto_now=True)
	winner = models.CharField(max_length=255, null=True)
	next_player_symbol = models.CharField(max_length=255, blank=True, default=PLAYER1)
	coordinate = models.IntegerField(null=True)
	closed = models.BooleanField(default=False)

	def move(self, position, player_symbol):
		if self.closed:
			raise Exception('This game is closed')
		if position < 0 or position > 8:
			raise Exception('Position must be an integer between 0 and 8')	
		if not self.position_available(position):
			raise Exception('This position is already used')		
		self.set_symbol(position, player_symbol)
		turn = Turn()
		turn.coordinate = position
		turn.player = player_symbol
		turn.game_id = self
		turn.save()
		if self.check_victory(player_symbol):
			self.closed = True
			self.winner = player_symbol
			self.save()
		if self.check_game_finish():
			self.closed = True
			self.winner = 'Tie'
			self.save()

	def check_game_finish(self):
		for i in range(len(self.current_state)):
			if self.current_state[i] == 'N':
				return False
		return True

	def position_available(self, position):
		symbol = self.current_state[position]
		return symbol not in [self.PLAYER1, self.PLAYER2]

	def set_symbol(self, position, player_symbol):
		self.current_state = self.current_state[:position] + player_symbol + self.current_state[position + 1:]
		self.next_player_symbol = 'X' if player_symbol == 'O' else 'O'
		self.save()

	def check_victory(self, player_symbol):
		assert player_symbol in [self.PLAYER1, self.PLAYER2]

		def check(position):
			return self.current_state[position] == player_symbol

		for i in range(0, 3):
			horizontal = check(0+i*3) and check(1+i*3) and check(2+i*3)
			vertical = check(0+i) and check(3+i) and check(6+i)
			if horizontal or vertical:
				return True

		if check(4) and ((check(0) and check(8)) or (check(2) and check(6))):
			return True

		return False
	
