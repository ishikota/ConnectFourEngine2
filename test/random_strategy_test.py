import os
import sys
PARENT_PATH = os.getcwd()[:-4]
sys.path.append(PARENT_PATH+'src/ui')
sys.path.append(PARENT_PATH+'src/strategy')
import unittest
import pdb
import bitboard
import random_strategy

class RandomStrategyTest(unittest.TestCase):

	def setUp(self):
		self.bb = bitboard.BitBoard(4,7,6)
		self.s1 = random_strategy.RandomStrategy(self.bb.FIRST)
		self.s2 = random_strategy.RandomStrategy(self.bb.SECOND)

	def test_random_choice(self):
		while True:
			col = self.s1.think(self.bb)	
			self.bb.update(self.s1.ME,col) 
			col = self.s2.think(self.bb)
			self.bb.update(self.s2.ME,col)
			if self.bb.checkDraw():
				self.bb.display()
				return
	
	def teatDown(self):
		print 'FINISH!!'

if __name__ == '__main__':
	unittest.main()
