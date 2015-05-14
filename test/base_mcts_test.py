import os
import sys
PARENT_PATH = os.getcwd()[:-4]
sys.path.append(PARENT_PATH+'src/ui')
sys.path.append(PARENT_PATH+'src/strategy')
import unittest
import bitboard
import base_mcts
import pdb
import game_manager
import time

class BaseMCTSTest(unittest.TestCase):

	def setUp(self):
		self.bb = bitboard.BitBoard(4,7,6)
		self.s1 = base_mcts.BaseMCTS(self.bb.FIRST)
		self.s2 = base_mcts.BaseMCTS(self.bb.SECOND)
		self.GM = game_manager.GameManager()

	def test_UCTSearch(self):
		print 'UCTSearch result is column '+str(self.s1.UCTSearch(self.bb))

	def test_if_overflow(self):
		self.GM.readBoard('base_mcts_1.in',self.bb)
		self.s2.D = True
		res = self.s2.think(self.bb)
		self.assertEqual(res,0)

	def test_treePolicy(self):
		root = base_mcts.Tree()
		self.s1.treePolicy(root, self.bb)
		self.s1.treePolicy(root, self.bb)
		self.s1.treePolicy(root, self.bb)
		self.s1.treePolicy(root, self.bb)
		self.s1.treePolicy(root, self.bb)
		self.s1.treePolicy(root, self.bb)
		self.s1.treePolicy(root, self.bb)
		#self.s1.expand(root, self.bb, 2)
	

	def test_expand(self):
		root = base_mcts.Tree()
		self.s1.expand(root, self.bb, 2)
		self.s1.expand(root, self.bb, 2)
		self.s1.expand(root, self.bb, 2)
		self.s1.expand(root, self.bb, 2)
		self.s1.expand(root, self.bb, 2)
		self.s1.expand(root, self.bb, 2)
		self.s1.expand(root, self.bb, 2)
		#self.s1.expand(root, self.bb, 2)

	def test_bestChild(self):
		root = base_mcts.Tree()
		root.update_num = 7
		root.children[0] = base_mcts.Tree()
		root.children[1] = base_mcts.Tree()
		root.children[2] = base_mcts.Tree()
		root.children[3] = base_mcts.Tree()
		root.children[4] = base_mcts.Tree()
		root.children[5] = base_mcts.Tree()
		root.children[6] = base_mcts.Tree()

		root.children[0].parent = root
		root.children[1].parent = root
		root.children[2].parent = root
		root.children[3].parent = root
		root.children[4].parent = root
		root.children[5].parent = root
		root.children[6].parent = root

		root.children[0].score = 10
		root.children[1].score = 20
		root.children[2].score = 5
		root.children[3].score = 50
		root.children[4].score = 70
		root.children[5].score = 1
		root.children[6].score = 0

		root.children[0].update_num = 1
		root.children[1].update_num = 1
		root.children[2].update_num = 1
		root.children[3].update_num = 1
		root.children[4].update_num = 1
		root.children[5].update_num = 1
		root.children[6].update_num = 1

		temp, res = self.s1.bestChild(root,0)
		self.assertEqual(res, 4)

	def test_default_policy(self):
		d = False
		t = base_mcts.Tree()
		for k in range(1000):
			self.bb = bitboard.BitBoard(4,7,6)
			res = self.s1.defaultPolicy(t,self.bb,self.bb.FIRST)
			may_draw = True
			for r in range(6):
				for c in range(7):
					p = (self.bb.FB >>(r*7+c)) & 1
					if p==1:
						if self.bb.check(r,c,self.bb.FIRST):
							self.assertEqual(res, 1,'res was '+str(res)+'(r,c)='+str(r)+','+str(c))
							if d:print 'First player win in (r,c)='+str(r)+','+str(c)
							may_draw = False
							break
					p = (self.bb.SB >>(r*7+c)) & 1
					if p==1:
						if self.bb.check(r,c,self.bb.SECOND):
							self.assertEqual(res, 0.01,'(r,c)='+str(r)+','+str(c))
							if d:print 'Second player win in (r,c)='+str(r)+','+str(c)
							may_draw= False
							break
			if may_draw and self.bb.checkDraw():
				if res == 0.01:
					self.bb.display()
				self.assertEqual(res, 0.5)
		# check the case when node is terminal
		t.is_terminal = True
		t.score = 255
		self.bb = bitboard.BitBoard(4,7,6)
		res = self.s1.defaultPolicy(t,self.bb,self.bb.FIRST)
		self.assertEqual(res, 255)
		print 'test_default_policy end'

	def test_backpropagation(self):
		root = base_mcts.Tree()
		c11 = base_mcts.Tree()
		c12 = base_mcts.Tree()
		c13 = base_mcts.Tree()
		c21 = base_mcts.Tree()
		c211 = base_mcts.Tree()
		# create tree
		c11.parent = root
		c12.parent = c11
		c13.parent = c12
		c21.parent = root
		c211.parent = c21
		self.s1.backPropagation(c211,0.01,4)
		self.s1.backPropagation(c13,1,2)
		
		#self.assertEqual(c11.score, 1)
		#self.assertEqual(c12.score,-1)
		
if __name__ == '__main__':
	unittest.main()

