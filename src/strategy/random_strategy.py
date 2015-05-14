from base_strategy import BaseStrategy

class RandomStrategy(BaseStrategy):
	
	def __init__(self, me):
		super(RandomStrategy, self).__init__(me)
	
	'''
	# Concrete method of thinking process.
	# Just return all possible moves here and
	# choose uniformly in BaseStrategy's randomChoice method.
	'''
	def makeANextMove(self, board):
		return range(board.WIDTH)
	
