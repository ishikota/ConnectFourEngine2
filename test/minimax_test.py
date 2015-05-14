import os
import sys
PARENT_PATH = os.getcwd()[:-4]
sys.path.append(PARENT_PATH+'src/ui')
sys.path.append(PARENT_PATH+'src/strategy')
import unittest
import bitboard
import minimax
import pdb
import game_manager
import time

class MinimaxTest(unittest.TestCase):

	def setUp(self):
		self.bb = bitboard.BitBoard(4,7,6)
		self.s1 = minimax.MiniMax(self.bb.FIRST)
		self.s1.setParam(3)
		self.s2 = minimax.MiniMax(self.bb.SECOND)
		self.s2.setParam(3)
		self.GM = game_manager.GameManager()

	def test_easy_choice(self):
		self.bb.update(2,3)
		self.bb.update(4,2)
		self.bb.update(2,3)
		self.bb.update(4,2)
		self.bb.update(2,3)
		self.bb.update(4,2)
		self.bb.display()
		c1 = self.s1.makeANextMove(self.bb)
		print c1
		print self.s2.makeANextMove(self.bb)
		self.assertEqual(len(c1), 1)
		self.assertEqual(c1[0],3)

	def test_easy_choice2(self):
		self.bb.update(4,3)
		self.bb.update(2,3)
		self.bb.update(4,2)
		self.bb.update(2,2)
		self.bb.update(4,4)
		self.bb.update(2,5)
		self.bb.display()
		c1 = self.s1.makeANextMove(self.bb)
		print c1
		print self.s2.makeANextMove(self.bb)

	def test_checkWin(self):
		self.GM.readBoard('get_row.in',self.bb)
		self.bb.display()
		ans = [False,True,False,False,False,True,False]
		for c in range(7):
			r = self.s2.getNextRow(self.bb.FB|self.bb.SB, c)
			res = self.s2.checkWin(self.bb.SB,r,c)
			self.assertEqual(ans[c], res,'failed in column '+str(c))
	
	def test_evalMove(self):
		self.GM.readBoard('get_row.in',self.bb)
		self.bb.display()
		print 'test_eval_move'
		for c in range(7):
			r = self.s1.getNextRow(self.bb.FB|self.bb.SB, c)
			score = self.s1.evalMove(1,self.bb.FB,self.bb.SB,2,r,c)
			print c,score

	def test_get_row(self):
		self.GM.readBoard('get_row.in',self.bb)
		self.bb.display()
		ans = [0,0,2,2,1,0,0]
		for i in range(self.bb.WIDTH):
			r = self.s1.getNextRow(self.bb.FB|self.bb.SB, i)
			self.assertEqual(r,ans[i],'expected '+str(ans[i])+' but '+str(r))
		
	def test_exe_time(self):
		print '**** START EXETIME TEST ***'
		for i in range(1,10):
			self.s1.setParam(i)
			st = time.time()
			self.s1.makeANextMove(self.bb)
			et = time.time()
			exe_time = et-st
			print 'Depth='+str(i)+', time='+str(exe_time)
			if exe_time > 20:
				break
		print '******END********'

if __name__ == '__main__':
	unittest.main()
