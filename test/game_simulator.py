import os
import sys

PARENT_PATH = os.getcwd()[:-4]
sys.path.append(PARENT_PATH+'ui')
sys.path.append(PARENT_PATH+'strategy')

import time
import bitboard
import game_manager

import minimax
import alphabeta
import iterative_deepening

class GameSimulator:

	def __init__(self):
		# return value for each game result
		self.DRAW_POINT = 0
		self.WIN_POINT = 1
		self.LOSE_POINT = 2
		self.d = True# if (d == True) then display game progress on shell

	'''
	@param
	w : the return value you want when you win
	d : the return value you want when you draw
	l : the return value you want when you lose
	'''
	def setReturnValue(self, w, d, l):
		self.WIN_POINT = w
		self.DRAW_POINT = d
		self.LOSE_POINT = l

	'''
	*** argument ***
	s1 : strategy for first player
	s2 : strategy for second player
	*** return(default) ***
	result :
		0  : draw
		1  : first player win
		2 : second player win
	'''
	def play(self, s1, s2):
		b = bitboard.BitBoard(4,7,6)
		t1, t2 = 0,0
		d = self.d
		turn = 0
		while True:
			turn += 1
			st = time.time()
			col = s1.think(b)
			et = time.time()
			t1 += et-st
			b.update(b.FIRST, col)
			if d: b.display()
			if b.check(b.getRow(col)-1, col, s1.ME):
				if d:print 'player1 average time:'+str(t1/(turn+1))
				if d:print 'player2 average time:'+str(t2/(turn))
				return self.WIN_POINT
			if b.checkDraw():
				if d:print 'player1 average time:'+str(t1/(turn+1))
				if d:print 'player2 average time:'+str(t2/(turn))
				return self.DRAW_POINT
			st = time.time()
			col = s2.think(b)
			et = time.time()
			t2 += et-st
			b.update(b.SECOND, col)
			if d: b.display()
			if b.check(b.getRow(col)-1, col, s2.ME):
				if d:print 'player1 average time:'+str(t1/(turn+1))
				if d:print 'player2 average time:'+str(t2/(turn))
				return self.LOSE_POINT
			if b.checkDraw():
				if d:print 'player1 average time:'+str(t1/(turn+1))
				if d:print 'player2 average time:'+str(t2/(turn))
				return self.DRAW_POINT

