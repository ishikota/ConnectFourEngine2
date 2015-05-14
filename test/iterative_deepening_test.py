import os
import sys
PARENT_PATH = os.getcwd()[:-4]
sys.path.append(PARENT_PATH+'src/ui')
sys.path.append(PARENT_PATH+'src/strategy')
import unittest
import bitboard
import iterative_deepening
import iterative_deepening2
import id_move_ordering
import id_mo_only_win
import id_tt
import pdb
import game_manager
import time
import random

class IterativeDeepeningTest(unittest.TestCase):

	def setUp(self):
		self.bb = bitboard.BitBoard(4,7,6)
		self.s1 = iterative_deepening.IterativeDeepening(self.bb.FIRST)
		self.s1.setParam(self.s1.DEPTH_LIMIT_MODE, 3)
		self.s2 = iterative_deepening.IterativeDeepening(self.bb.SECOND)
		self.s2.setParam(self.s2.DEPTH_LIMIT_MODE, 3)
		self.GM = game_manager.GameManager()

	def test_tt(self):
		s = id_tt.IterativeDeepening(self.bb.FIRST)
		s.setParam(s.DEPTH_LIMIT_MODE, 10)
		print s.think(self.bb)

	def test_update_key(self):
		s = id_tt.IterativeDeepening(self.bb.FIRST)
		c = random.randint(0,6)
		r = 0
		z = s.zobrist[r][c][1]
		old_key = s.computeKey(self.bb.FB, self.bb.SB)
		new_key = s.updateKey(old_key, r, c, 1)
		self.assertEqual(old_key^z, new_key)

	def test_compute_key(self):
		s = id_tt.IterativeDeepening(self.bb.FIRST)
		empty_key = s.computeKey(self.bb.FB, self.bb.SB)
		self.bb.update(self.bb.FIRST, 0)
		new_key = s.computeKey(self.bb.FB, self.bb.SB)
		z = s.zobrist[0][0][1]
		self.assertEqual(empty_key^z, new_key)

	def test_zobrist_key(self):
		s = id_tt.IterativeDeepening(self.bb.FIRST)
		key1 = s.computeKey(self.bb.FB, self.bb.SB)
		key2 = s.computeKey(self.bb.FB, self.bb.SB)
		self.assertEqual(key1,key2)

		c = random.randint(0,6)
		r = 0
		key1 = s.updateKey(key1, r, c, 1)
		key1 = s.updateKey(key1, r, c, 1)
		self.assertEqual(key1, key2)

		key1 = s.updateKey(key1, r, c, 1)
		before = self.bb.FB
		self.bb.update(self.bb.FIRST, c)
		after = self.bb.FB
		self.bb.display()
		key2 = s.computeKey(self.bb.FB, self.bb.SB)
		self.assertEqual(key1,key2, bin(key1)+', '+bin(key2))

	def test_search_depth(self):
		st, et = 0,0
		s1 = id_move_ordering.IterativeDeepening(self.bb.FIRST)
		s1.D = True
		s1.setParam(self.s1.DEPTH_LIMIT_MODE, 11)
		st = time.time()
		s1.makeANextMove(self.bb)
		killer_time = (time.time() - st)
		s2 = iterative_deepening.IterativeDeepening(self.bb.FIRST)
		s2.setParam(s2.DEPTH_LIMIT_MODE, 11)
		st = time.time()
		s2.makeANextMove(self.bb)
		original_time = (time.time() - st)
		s3 = id_tt.IterativeDeepening(self.bb.FIRST)
		s3.setParam(s3.DEPTH_LIMIT_MODE, 11)
		s3.D = True
		st = time.time()
		s3.makeANextMove(self.bb)
		tt_time = (time.time() - st)
		
		print 'Compare time result'
		print 'original : '+str(original_time)+' (s)'
		print 'ordering : '+str(killer_time)+' (s)'
		print 'transpos : '+str(tt_time)+' (s)'

	def test_thinking_time(self):
		depth = 10
		st, et = 0,0
		self.GM.readBoard('3-ply-win-first.in', self.bb)
		s1 = id_move_ordering.IterativeDeepening(self.bb.FIRST)
		s1.setParam(self.s1.DEPTH_LIMIT_MODE, depth)
		st = time.time()
		s1.makeANextMove(self.bb)
		killer_time = (time.time() - st)
		s2 = iterative_deepening.IterativeDeepening(self.bb.FIRST)
		s2.setParam(self.s2.DEPTH_LIMIT_MODE, depth)
		st = time.time()
		s2.makeANextMove(self.bb)
		original_time = (time.time() - st)
		s3 = id_mo_only_win.IterativeDeepening(self.bb.FIRST)
		s3.setParam(s3.DEPTH_LIMIT_MODE, depth)
		st = time.time()
		s3.makeANextMove(self.bb)
		only_win_time = (time.time() - st)
		s4 = id_tt.IterativeDeepening(self.bb.FIRST)
		s4.setParam(s4.DEPTH_LIMIT_MODE, depth)
		st = time.time()
		s4.makeANextMove(self.bb)
		tt_time = (time.time() - st)

		print 'Compare time result'
		print 'original : '+str(original_time)+' (s)'
		print 'ordering : '+str(killer_time)+' (s)'
		print 'only win : '+str(only_win_time)+' (s)'
		print 'transpos : '+str(tt_time)+' (s)'

	def test_move_ordering(self):
		self.GM.readBoard('3-ply-win-first.in', self.bb)
		s = id_move_ordering.IterativeDeepening(self.bb.FIRST)
		s.setParam(self.s1.DEPTH_LIMIT_MODE, 9)
		s.makeANextMove(self.bb)

	def test_sort_killermove(self):
		s = id_move_ordering.IterativeDeepening(self.bb.FIRST)
		killer_move = [(40,3),(35,5)]
		arranged_moves = s.moveOrdering(killer_move)
		self.assertEqual([3,5,0,1,2,4,6], arranged_moves, 'arranged_moves is'+str(arranged_moves)+'(should be [3,5,1,2,4,6])')

	def test_update_killermove(self):
		s = id_move_ordering.IterativeDeepening(self.bb.FIRST)
		move = 4
		# second update
		killer_move = [(40,3),(30,5)]
		score = 35
		s.updateKillerMove(killer_move, move, score) 
		self.assertEqual(killer_move, [(40,3), (35,4)])
		#best update
		killer_move = [(40,3),(30,5)]
		score = 42
		s.updateKillerMove(killer_move, move, score) 
		self.assertEqual(killer_move, [(42,4),(40,3)])
		# swap update
		move = 5
		killer_move = [(40,3),(30,5)]
		s.updateKillerMove(killer_move, move, score) 
		self.assertEqual(killer_move, [(42,5),(40,3)])
		# no update
		move = 6
		score = -20
		killer_move = [(40,3),(30,5)]
		s.updateKillerMove(killer_move, move, score) 
		self.assertEqual(killer_move, [(40,3),(30,5)])
		# depulicate case 1
		move = 3
		score = 42
		killer_move = [(40,3),(30,5)]
		s.updateKillerMove(killer_move, move, score) 
		self.assertEqual(killer_move, [(42,3),(30,5)])
		# depulicate case 2
		move = 3
		score = 35
		killer_move = [(40,3),(30,5)]
		s.updateKillerMove(killer_move, move, score) 
		self.assertEqual(killer_move, [(40,3),(30,5)])


	def test_a_start(self):
		s = iterative_deepening2.IterativeDeepening(self.bb.FIRST)
		s.setParam(s.DEPTH_LIMIT_MODE, 9)
		mb = self.bb.FB
		ob = self.bb.SB
		for c in range(7):
			r = self.bb.getRow(c)
			s.ALPHA_MEMO, s.BETA_MEMO = -100, 100
			m = 1<<(r*7+c)
			s.evalMove(9, 1, mb|m, ob, s.ME, r, c, -100, 100)
			print 'column '+str(c)+': alpha ='+str(s.ALPHA_MEMO)+',beta='+str(s.BETA_MEMO)

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
	
	def test_exe_time(self):
		print '**** START EXETIME TEST ***'
		for i in range(1,15):
			self.s1.setParam(self.s1.DEPTH_LIMIT_MODE, i)
			st = time.time()
			self.s1.makeANextMove(self.bb)
			et = time.time()
			exe_time = et-st
			print 'Depth='+str(i)+', time='+str(exe_time)
			if exe_time > 10:
				break
		print '******END********'

	def test_exe_time_mo(self):
		print '**** START EXETIME TEST (MoveOrdering) ***'
		s1 = id_move_ordering.IterativeDeepening(self.bb.FIRST)
		for i in range(1,15):
			s1.setParam(s1.DEPTH_LIMIT_MODE, i)
			st = time.time()
			s1.makeANextMove(self.bb)
			et = time.time()
			exe_time = et-st
			print 'Depth='+str(i)+', time='+str(exe_time)
			if exe_time > 10:
				break
		print '******END********'

	def test_exe_time_tt(self):
		print '**** START EXETIME TEST (Transpotition Table) ***'
		s1 = id_tt.IterativeDeepening(self.bb.FIRST)
		for i in range(1,15):
			s1.setParam(s1.DEPTH_LIMIT_MODE, i)
			st = time.time()
			s1.makeANextMove(self.bb)
			et = time.time()
			exe_time = et-st
			print 'Depth='+str(i)+', time='+str(exe_time)
			if exe_time > 10:
				break
		print 'Depth='+str(i)+', time='+str(exe_time)

	def test_exe_time_only_win(self):
		print '**** START EXETIME TEST (Transpotition Table) ***'
		s1 = id_mo_only_win.IterativeDeepening(self.bb.FIRST)
		for i in range(1,15):
			s1.setParam(s1.DEPTH_LIMIT_MODE, i)
			st = time.time()
			s1.makeANextMove(self.bb)
			et = time.time()
			exe_time = et-st
			print 'Depth='+str(i)+', time='+str(exe_time)
			if exe_time > 10:
				break
		print 'Depth='+str(i)+', time='+str(exe_time)

if __name__ == '__main__':
	unittest.main()


