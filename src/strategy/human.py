import os
import sys
PARENT_PATH = os.getcwd()[:-8]
sys.path.append(PARENT_PATH+'ui')
import game_manager
from base_strategy import BaseStrategy

class Human(BaseStrategy):

	def __init__(self, me):
		super(Human, self).__init__(me)
		self.GM= game_manager.GameManager()
	
	def makeANextMove(self, board):
		player_char = 'O' if self.ME == board.FIRST else 'X' 
		player_str = ('FIRST' if self.ME == board.FIRST else 'SECOND' )+ ' PLAYER ('+player_char+')'
		col = self.GM.getInput(player_str, board)
		return [col]

