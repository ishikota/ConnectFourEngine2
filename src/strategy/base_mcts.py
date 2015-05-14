from base_strategy import BaseStrategy
import time
import math
from sys import stdout
import pdb
import random_strategy
'''
This class represents node of search tree.
'''
class Tree:
	def __init__(self):
		self.CHILD_NUM = 7
		self.parent = -1
		self.children = [-1 for i in range(self.CHILD_NUM)]
		self.score = 0
		self.update_num = 0
		self.unvisited = self.CHILD_NUM # number of unvisted children
		self.is_terminal = False

class BaseMCTS(BaseStrategy):

	def __init__(self, me):
		super(BaseMCTS, self).__init__(me)
		self.PLAYOUT_LIMIT_MODE = 0
		self.TIME_LIMIT_MODE = 1
		self.MODE = self.PLAYOUT_LIMIT_MODE
		self.PLAYOUT_LIMIT = 1000
		self.MY_STRATEGY = random_strategy.RandomStrategy(self.ME)
		self.OPPO_STRATEGY = random_strategy.RandomStrategy(self.OPPO)
		self.OVERFLOW_FLG = False # check if overflow occured on UCT value.(Threshold is 1<<16.)

	def setParameter(self, playout_num):
		if self.MODE == self.PLAYOUT_LIMIT_MODE:
			self.PLAYOUT_LIMIT = max(10, playout_num)
		elif self.MODE == self.TIME_LIMIT_MODE:
			self.PLAYOUT_LIMIT = max(0.1, playout_num)

	def makeANextMove(self, board):
		self.OVERFLOW_FLG = False
		best_moves = self.UCTSearch(board)
		return [best_moves]	

	# grow a MCTS tree and choose best root child.
	def UCTSearch(self, board):
		v_0 = Tree() # root node
		play_counter = 0
		memo = (board.FB, board.SB, board.POS)

		st = time.time()
		nt = st
		while True:
			if (self.MODE == self.PLAYOUT_LIMIT_MODE and play_counter  < self.PLAYOUT_LIMIT) or\
					(self.MODE == self.TIME_LIMIT_MODE and (nt-st) > self.PLAYOUT_LIMIT):
						break
			stdout.flush()
			stdout.write("\r  thinking...(%d/%d)" % (play_counter+1,self.PLAYOUT_LIMIT))
			board.FB, board.SB, board.POS = memo # reset board state
			v_l, next_player = self.treePolicy(v_0, board)
			delta = self.defaultPolicy(v_l, board, next_player)
			self.backPropagation(v_l, delta, next_player)
			play_counter += 1
			if self.OVERFLOW_FLG:
				if self.D: print 'Overflow detected.'
				break
			nt = time.time()

		board.FB, board.SB, board.POS = memo # reset board state
		stdout.write("\n")
		# choose best child of root node.
		for child in v_0.children:
			if child == -1 or child == -2: continue
			if self.D : print 'column:'+str(v_0.children.index(child))+\
					' score:'+str(child.score)+' update:'+str(child.update_num)
		tmp, best_action = self.bestChild(v_0, 0)
		return best_action

	'''
	*argument
	* v : root node of search tree
	* board : current state of child node which we are now focusing
	* return
	* v_l : leaf node of search tree
	* board : this board state is already updated to leaf node state.
	* next_player : next player to play after leaf node state
	'''
	def treePolicy(self, v, board):
		# while v is non-terminal node
		next_player = self.ME
		while not v.is_terminal:
			if v.unvisited!= 0:
				return self.expand(v, board, next_player)
			else: # If all child nodes are visited, descends the tree toward best child node.
				c = 1.0/math.sqrt(2) # constant for adjustment
				v, column = self.bestChild(v,c)
				board.update(next_player, column)
				next_player = self.OPPO if next_player == self.ME else self.ME
		return v, next_player

	def expand(self, v, board, next_player):
		# choose un-tried action
		action = 0
		while True:
			action = v.children.index(-1)
			v.unvisited -=1
			# if rest of un-tried action is infeasible(which make a move on full-stacked column),
			# this means that this node have already finished expanding process.
			# So jump to choose best-child process which we do after expanding process.
			if board.getRow(action) == board.HEIGHT:
				v.children[action] = -2 # -2 indicates that this move is infeasible.
				if v.unvisited == 0:
					return self.treePolicy(v, board)
			else:
				break
		# add a new child node to v
		v_child = Tree()
		v_child.parent = v
		row = board.getRow(action)
		board.update(next_player, action)
		if board.check(row, action,next_player):
			v_child.is_terminal = True
			v_child.score = 1 if next_player == self.ME else -1
		elif board.checkDraw():
			v_child.is_terminal = True
			v_child.score = 0
		v.children[action] = v_child
		next_player = self.OPPO if next_player == self.ME else self.ME
		return v_child, next_player

	# select a child node which got highest UCT value
	def bestChild(self, v, c):
		best_val = 0
		is_first = True
		for i in range(7): # board width
			child = v.children[i]
			if child == -2: continue # if this action is infeasible(put a move on full-stacked column)
			UCTvalue = self.calcUCTvalue(child, c)
			if UCTvalue > best_val or is_first:
				best_val = UCTvalue
				best_index = i
				is_first = False
		return v.children[best_index], best_index

	def calcUCTvalue(self, child, c):
		exploitation_term = 1.0*child.score/child.update_num
		exploration_term = c*math.sqrt(2*math.log(child.parent.update_num)/child.update_num)
		UCTvalue = exploitation_term + exploration_term
		if UCTvalue > 1<<16:
			self.OVERFLOW_FLG = True
			if self.D: print 'Overflow occured!!'
		return UCTvalue

	def defaultPolicy(self, v_l, board, next_player):
		# win = 1pt , draw = 0.5pt, lose = 0.01pt
		if v_l.is_terminal:
			return v_l.score
		# start simulation
		while True:
			is_me = next_player == self.ME
			s = self.MY_STRATEGY if is_me else self.OPPO_STRATEGY
			col = s.think(board)
			row = board.getRow(col)
			board.update(next_player, col)
			if board.check(row, col, next_player):
				return 1 if is_me else 0.01
			elif board.checkDraw():
				return 0.5
			next_player = self.OPPO if is_me else self.ME

	# backup the result score of simulation from leaf node to root node.
	def backPropagation(self, v, delta, next_player):
		# if v_l node is minimizer node, 
		# inverse sign of delta(reward) for negamax
		delta = -delta if next_player == self.ME else delta 
		while True: # ascends tree to the root node
			v.update_num += 1
			v.score += delta
			v = v.parent
			delta = -delta # doing negaMax here
			if v == -1: break

