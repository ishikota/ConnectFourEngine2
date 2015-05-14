import abc
import random

'''
# All strategy class like MiniMax, AlphaBeta, ...
# extends this base class and implement their own
# thinking method in makeANextMove method
'''
class BaseStrategy(object):
	__metaclass__ = abc.ABCMeta

	def __init__(self, me):
		self.ME = me # ME   is the piece of player who use this strategy.
		self.OPPO = 4 if me == 2 else 2 # OPPO is the piece of opponent (against ME.)
		self.D = False # D is debug flag
		# variable for check function$
		self.R_MASK  = int('111111011111101111110111111011111101111110', 2)
		self.L_MASK  = int('011111101111110111111011111101111110111111', 2)
		self.UR_MASK = int('111111011111101111110111111011111111111111', 2)
		self.LL_MASK = int('111111111111110111111011111101111110111111', 2)
		self.UL_MASK = int('011111101111110111111011111101111110111111', 2)
		self.LR_MASK = int('111111011111101111110111111011111101111110', 2)

	'''
	# This method is abstract method.
	# Return next move's row and column position. 
	# by following subclass's strategy.
	# Return -1, -1 , if cannot find good move.
	# then next move is chosen randomly.
	'''
	@abc.abstractmethod
	def makeANextMove(self, board):
		pass

	'''
	# This method is called when all of next move's score is same,
	# choice next move randomly.
	# (But do not choice the columns which already full-stacked.)
	'''
	def randomChoice(self, board, best_moves):
		if len(best_moves)==1:
			return best_moves[0]
		random.shuffle(best_moves)
		for col in best_moves:
			if board.getRow(col) != board.HEIGHT:
				return col

	'''
	# This method is abstract method.
	# sub class implements this method to
	# adjut strategy parameter from main program.
	'''
	def setParameter(self):
		pass

	'''
	# This method is called from main loop.
	# Subclass implements thinking process.
	'''
	def think(self, board):
		best_moves = self.makeANextMove(board)
		if self.D: print 'BEST MOVES : '+str(best_moves)
		return self.randomChoice(board, best_moves)

	def getNextRow(self, bb, c):
		tmp = bb>>c
		for i in range(6): # board.HEIGHT
			if tmp&1 == 0: return i
			tmp = tmp>>7 # board.WIDTH
		return 6 # board.HEIGHT
		
	def checkWin(self, bb, r, c):
		m = 1<<(r*7+c)
		# check 7 direction
		num = 1
		for k in range(7):
			mask = self.transfer(m, k)
			for i in range(3):
				if mask==0 or mask&bb==0: break
				num += 1
				mask = self.transfer(mask,k)
			if (k==1 or k==3 or k==5 or k==6):
				if num>=4: return True
				else: num = 1
		return False

	def transfer(self, m, d):
		if d == 0: return (m<<1) & self.R_MASK # right direction
		if d == 1: return (m>>1) & self.L_MASK # left direction$
		#if d == 2: return (m<<7) # upper direction$
		if d == 2: return (m<<(7+1)) & self.UR_MASK # upper right$
		if d == 3: return (m>>(7+1)) & self.LL_MASK # lower left$
		if d == 4: return (m<<(7-1)) & self.UL_MASK # upper left$
		if d == 5: return (m>>(7-1)) & self.LR_MASK # lower right$
		if d == 6: return (m>>7) # lower directiond



