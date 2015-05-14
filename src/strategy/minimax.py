from base_strategy import BaseStrategy
import pdb

class MiniMax(BaseStrategy):

	def __init__(self, me):
		super(MiniMax, self).__init__(me)
		self.MAX_DEPTH = 2
		
	def setParam(self, depth):
		if depth == 0:
			raise Exception('set MAX_DEPTH = 0 is not allowed.')
		self.MAX_DEPTH = depth
	
	'''
	Concrete method of thinking process.
	return array of column of best moves.
	'''
	def makeANextMove(self, board):
		best_memo = 0
		best_num = 0
		best_score = -100 # negative inf
		mb = board.FB if self.ME == board.FIRST else board.SB
		ob = board.SB if mb == board.FB else board.FB
		for c in range(board.WIDTH):
			r = board.getRow(c)
			if r == board.HEIGHT:continue
			m = 1<<(r*board.WIDTH+c)
			temp_score = self.evalMove(1, mb|m, ob, self.ME, r, c)
			if self.D: print 'column'+str(c)+' : score='+str(temp_score)
			if temp_score > best_score:
				best_score = temp_score
				best_memo = 1<<c
				best_num = 1
			elif temp_score == best_score:
				best_memo |= 1<<c
				best_num += 1

		best_moves =[0 for i in range(best_num)]
		index = 0
		for c in range(board.WIDTH):
			if best_memo & 1:
				best_moves[index] = c
				index +=1
			best_memo = best_memo>>1
		return best_moves

	def evalMove(self, depth, mb, ob, player, row, col):
		# gives good score to winning move found in early turn
		if self.checkWin(mb, row, col):
			if player == self.ME: return 42-depth
			else: return -(42-depth)

			# reached to computational budget
		if depth == self.MAX_DEPTH: return 0

		next_player = self.ME if player == self.OPPO else self.OPPO
		best_score = 0 # replcement of negative inf
		is_first = True
		for c in range(7): # board.WIDTH
			r = self.getNextRow(mb|ob, c)
			if r == 6: continue # board.HEIGHT
			m = 1<<(r*7+c) # r*board.WIDTH+c
			temp_score = self.evalMove(depth+1, ob|m, mb, next_player, r, c)
			if is_first:
				best_score = temp_score
				is_first = False
			elif player == self.ME:
				best_score = min(temp_score, best_score)
			else:
				best_score = max(temp_score, best_score)
		return best_score

