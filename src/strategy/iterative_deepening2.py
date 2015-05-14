from base_strategy import BaseStrategy
import time

class IterativeDeepening(BaseStrategy):

	def __init__(self, me):
		super(IterativeDeepening, self).__init__(me)
		self.DEPTH_LIMIT_MODE = 0
		self.TIME_LIMIT_MODE = 1
		self.MODE = self.DEPTH_LIMIT_MODE
		# memo for a* search
		self.BEST_ALPHA = [-100 for i in range(7)]
		self.BEST_BETA = [100 for i in range(7)]
		self.ALPHA_MEMO = -100
		self.BETA_MEMO = 100
	'''
	set strategy-specific parameter.
	mode  : the kind of computational budget for iterative deepening.
	limit : computational budget for iterative deepening.
	'''
	def setParam(self, mode, limit):
		self.MODE = mode
		self.LIMIT = limit

	'''
	Concrete method of thinking process.
	return array of column of best moves.
	This strategy implements a* algorithm which search the column first
	which has good alpha or beta value.
'''
	def makeANextMove(self, board):
		# initialize
		mb = board.FB if self.ME == board.FIRST else board.SB
		ob = board.SB if mb == board.FB else board.FB
		#valiable for IterativeDeepening
		depth_limit = 1
		solved = 0 #  bit flg. if score of column c is solved, c-bit becomes 1
		scores = [0 for i in range(7)] # board.WIDTH
		st = time.time()
		nt = st
		for i in range(7): self.BEST_ALPHA[i] = -100
		for i in range(7): self.BEST_BETA[i] = 100

		while True:
			for c in range(board.WIDTH):
				r = board.getRow(c)
				if (solved>>c)&1:
					if self.D: print 'already solved column '+str(c)+', so do not search here'
					continue
				if r == board.HEIGHT:
					solved |= 1<<c
					scores[c] = -100 # big negative number
					continue
				
				self.ALPHA_MEMO, self.BETA_MEMO = -100, 100
				m = 1<<(r*board.WIDTH+c)
				temp_score = self.evalMove(depth_limit, 1, mb|m, ob, self.ME, r, c, -100, 100)
				if self.D: print 'column'+str(c)+' : score='+str(temp_score)
				if temp_score != 0:
					solved |= 1<<c
					scores[c] = temp_score
				self.BEST_ALPHA[c], self.BEST_BETA[c] = self.ALPHA_MEMO, self.BETA_MEMO
				if self.D: print 'column'+str(c)+' : alpha='+str(self.BEST_ALPHA[c])+',beta='+str(self.BEST_BETA[c])
			if solved == (1<<7)-1 or depth_limit == 42:
				break

			# break loop if it reaches to computational budget
			if (self.MODE == self.DEPTH_LIMIT_MODE and depth_limit == self.LIMIT) or\
					(self.MODE == self.TIME_LIMIT_MODE and (nt-st) > self.LIMIT):
						break
			# else prepare to next loop
			depth_limit += 1
			nt = time.time()
		
		if self.D: print 'current search depth was '+str(depth_limit)
		best_score = max(scores)
		best_moves = []
		for c, score in enumerate(scores):
			if score == best_score: best_moves.append(c)
		return best_moves

	def evalMove(self, depth_limit, depth, mb, ob, player, row, col, _alpha, _beta):
		alpha, beta = _alpha, _beta
		if self.checkWin(mb, row, col):
			if player == self.ME: return 42-depth
			else: return -(42-depth)
		
		if depth == depth_limit: return 0

		next_player = self.ME if player == self.OPPO else self.OPPO
		best_score = 0
		is_first = True
		for c in range(7): # board.WIDTH
			r = self.getNextRow(mb|ob, c)
			if r == 6: continue # board.HEIGHT
			m = 1<<(r*7+c) # r*board.WIDTH+c
			temp_score = self.evalMove(depth_limit, depth+1, ob|m, mb, next_player, r, c, alpha, beta)
			
			if next_player == self.OPPO: # if this node is minimizer node
				if temp_score <= alpha:
					return temp_score
				if temp_score < beta: # update beta value
					beta = temp_score
					self.BETA_MEMO = temp_score
			else: # if this node is maximizer node
				if temp_score >= beta:
					return temp_score
				if temp_score > alpha:
					alpha = temp_score
					self.ALPHA_MEMO = temp_score
			
			if is_first:
				best_score = temp_score
				is_first = False
			elif player == self.ME:
				best_score = min(temp_score, best_score)
			else:
				best_score = max(temp_score, best_score)
			
		return best_score

