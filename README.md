# tic_tac_toe

http://localhost:8000/

Each position of the board has a number between 0 to 8, from left to right and from top to bottom.

012
345
678

/newgame/ - start a new game for two players: X and O. Returns the new game id and board_state:

{
    "id": id,
    "board_state": board_state
}

/maketurn/ - make a move in a play. First move make a 'X'-player, like in a standart version of the game. Input: id, player_symbol, position. Return the board state and next player symbol, or a winner name in the end of game.

{
    "board_state": board_state, 
    "next_player_symbol": next_player_symbol
}

{
    "board_state": closed, 
    "winner": winner
}

/getturns/ - return all the turns by game id.

[
    {
        "id": id,
        "game_id": game_id,
        "player_symbol": player_symbol,
        "coordinate": position
    },
	...
]

