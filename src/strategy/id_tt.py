from base_strategy import BaseStrategy
import time
import random
'''
This strategy uses iterative deepening with transposition table.
'''
class IterativeDeepening(BaseStrategy):

	def __init__(self, me):
		super(IterativeDeepening, self).__init__(me)
		self.DEPTH_LIMIT_MODE = 0
		self.TIME_LIMIT_MODE = 1
		self.MODE = self.DEPTH_LIMIT_MODE
		# save 2 killer moves for each depth.(we allocate array for 20 depth)
		self.killer_moves = [[(-100, j) for j in range(2)] for i in range(20)]
		self.initTT()

	'''
	set strategy-specific parameter.
	mode  : the kind of computational budget for iterative deepening.
	limit : computational budget for iterative deepening.
	'''
	def setParam(self, mode, limit):
		self.MODE = mode
		self.LIMIT = limit

	def initTT(self):
		self.TT = {}
		self.zobrist = self.generateZobristElem()

	def computeKey(self, mb, ob):
		hash_key = 0
		for r in range(6):
			for c in range(7):
				if mb&1:
					hash_key ^= self.zobrist[r][c][1]
				elif ob&1:
					hash_key ^= self.zobrist[r][c][2]
				else:
					pass#hash_key ^= self.zobrist[r][c][0]
				mb = mb>>1
				ob = ob>>1
		return hash_key

	'''
	update key by doing XOR operation on old key by zobrist element update-move
	old_key : current zobrist key which attached to current board configuration
	row     : row of update move
	col     : column of update move
	player  : player to make an update move.(1-> first player, 2-> second player)
	@return : new zobrist key which attached to updated board configuration
	'''
	def updateKey(self, old_key, row, col, player):
		return old_key ^ self.zobrist[row][col][player]
 
	def generateZobristElem(self):
		# k : flg of player. 0->empty, 1->first player, 2-> second player
		# c : column of square
		# r : row of square
		zobrist = [[[0 for k in range(3)] for j in range(7)] for i in range(6)]
		for r in range(6):
			for c in range(7):
				for p in range(3):
					zobrist[r][c][p] = random.randint(0,1<<20)
		return zobrist

	'''
	find transposition information from TT.
	return tuple of its information else -1 as flg.

	entry format
	(secondary_key, depth, score, flg, best_move)
	secondary_key : key to avoid the situation that different board state has same hash
	depth : search ply of stored depth
	score : score
	flg   : indicates the score is dinite score or upper/lower bound
	best_move : best next move from this move
	alpha : alpha value when this score was calculated
	beta  : beta value when this score was calculated
	'''
	def checkIfKeyExists(self, mb, ob):
		key = self.computeKey(mb, ob)
		if key in self.TT:
			entry = self.TT[key]
			return entry
		else:
			return -1

	def storeSearchResult(self, mb, ob, depth, score, flg, best_move, alpha, beta):
		key = self.computeKey(mb, ob)
		self.TT[key] = (0, depth, score, flg, best_move, alpha, beta)

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
		self.TT = {}
		self.tt_hit = 0
		self.eval_count = 0
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
		if self.D: print 'transposition hit was '+str(self.tt_hit)+'/'+str(self.eval_count)
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
		moves = self.moveOrdering(self.killer_moves[depth])
		for c in moves: # board.WIDTH
			r = self.getNextRow(mb|ob, c)
			if r == 6: continue # board.HEIGHT
			m = 1<<(r*7+c) # r*board.WIDTH+c

			# Start : transposition table specific code
			self.eval_count += 1
			temp_score = 0
			fb = mb if player == self.ME else ob|m
			sb = ob|m if player == self.ME else mb
			update_key = self.computeKey(fb, sb)
			entry_exists = False
			entry = self.TT[update_key] if update_key in self.TT else -1
			if entry != -1 and entry[1] >= depth_limit - depth: # entry[1] : depth
				if entry[5] <= alpha and beta <= entry[6]: # entry[5] : tt_alpha, entry[6] : tt_beta
					temp_score = entry[2] # entry[2] : evaluated score
					entry_exists = True
					self.tt_hit += 1
			if not entry_exists:
				temp_score = self.evalMove(depth_limit, depth+1, ob|m, mb, next_player, r, c, alpha, beta)
				self.storeSearchResult(fb,sb,depth_limit-depth,temp_score,0,0,alpha, beta)
			# End   : transposition table specific code
			
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

