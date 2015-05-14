from base_strategy import BaseStrategy
import time

class IterativeDeepening(BaseStrategy):

	def __init__(self, me):
		super(IterativeDeepening, self).__init__(me)
		self.DEPTH_LIMIT_MODE = 0
		self.TIME_LIMIT_MODE = 1
		self.MODE = self.DEPTH_LIMIT_MODE
		# save 2 killer moves for each depth.(we allocate array for 20 depth)
		self.killer_moves = [[(-100, j) for j in range(2)] for i in range(20)]
	
	'''
	set strategy-specific parameter.
	mode  : the kind of computational budget for iterative deepening.
	limit : computational budget for iterative deepening.
	'''
	def setParam(self, mode, limit):
		self.MODE = mode
		self.LIMIT = limit

	# killer move is tuple of (score, column)
	def moveOrdering(self, killer_move):
		moves = range(7) # board.WIDTH
		moves[0] = killer_move[0][1]
		moves[1] = killer_move[1][1]
		index = 2
		for i in range(7):
			if i == moves[0] or i == moves[1]: continue
			moves[index] = i
			index += 1
		return moves

	# killer move is tuple of (score, column)
	def updateKillerMove(self, killer_move, move, score):
		best, second = killer_move[0][0], killer_move[1][0]
		if score >= best:
			if killer_move[0][1] == move:
				killer_move[0] = (score, move)
			else:
				killer_move[1] = killer_move[0]
				killer_move[0] = (score, move)
		elif score >= second:
			if killer_move[0][1] != move:
				killer_move[1] = (score, move)

	'''
	Concrete method of thinking process.
	return array of column of best moves.
	'''
	def makeANextMove(self, board):
		mb = board.FB if self.ME == board.FIRST else board.SB
		ob = board.SB if mb == board.FB else board.FB
		#valiable for IterativeDeepening
		depth_limit = 1
		solved = 0 #  bit flg. if score of column c is solved, c-bit becomes 1
		scores = [0 for i in range(7)] # board.WIDTH
		st = time.time()
		nt = st

		# save 2 killer moves for each depth.(we allocate array for 20 depth)
		self.killer_moves = [[(-100, j) for j in range(2)] for i in range(20)]
		while True:
			moves = self.moveOrdering(self.killer_moves[0])
			print 'orderd move = '+str(moves)
			for c in moves:
				r = board.getRow(c)
				if (solved>>c)&1:
					continue
				if r == board.HEIGHT:
					solved |= 1<<c
					scores[c] = -100 # big negative number
					continue
				
				m = 1<<(r*board.WIDTH+c)
				temp_score = self.evalMove(depth_limit, 1, mb|m, ob, self.ME, r, c, -100, 100)
				#if self.D: print 'column'+str(c)+' : score='+str(temp_score)
				if temp_score != 0:
					solved |= 1<<c
					scores[c] = temp_score
					self.updateKillerMove(self.killer_moves[0], c, temp_score)
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
			if player == self.ME: return 1
			else: return -1
		
		if depth == depth_limit: return 0

		next_player = self.ME if player == self.OPPO else self.OPPO
		best_score = 0
		is_first = True
		moves = self.moveOrdering(self.killer_moves[depth])
		for c in moves: # board.WIDTH
			r = self.getNextRow(mb|ob, c)
			if r == 6: continue # board.HEIGHT
			m = 1<<(r*7+c) # r*board.WIDTH+c
			temp_score = self.evalMove(depth_limit, depth+1, ob|m, mb, next_player, r, c, alpha, beta)
			
			if next_player == self.OPPO: # if this node is minimizer node
				if temp_score <= alpha:
					return temp_score
				if temp_score < beta: # update beta value
					beta = temp_score
					self.updateKillerMove(self.killer_moves[depth], c, temp_score)
			else: # if this node is maximizer node
				if temp_score >= beta:
					return temp_score
				if temp_score > alpha:
					alpha = temp_score
					self.updateKillerMove(self.killer_moves[depth], c, temp_score)
			
			if is_first:
				best_score = temp_score
				is_first = False
			elif player == self.ME:
				best_score = min(temp_score, best_score)
			else:
				best_score = max(temp_score, best_score)
			
		return best_score

