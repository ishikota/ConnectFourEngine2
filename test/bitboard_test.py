import os
import sys
PARENT_PATH = os.getcwd()[:-4]
sys.path.append(PARENT_PATH+'src/ui')

import unittest
import bitboard
import pdb

class BitboardTest(unittest.TestCase):

	def setUp(self):
		self.bb = bitboard.BitBoard(4,7,6)
	
	def test_display(self):
		self.bb.display()
	
	def test_win_check(self):
		b = self.bb
		test_moves = [
				[1,1,2,2,3,4,0], # right direction
				[1,1,2,2,0,0,3], # left direction
				[3,2,3,2,3,2,3], # lower direction (vertical line)
				[0,4,3,5,4,5,6,6,5,6,6], # lower left
				[0,4,4,5,5,6,5,6,0,6,6,0,3], # upper right
				[4,3,3,2,1,2,2,1,0,1,1], # lower right
				[0,0,0,1,0,1,1,2,2,4,3], # upper left
				[3,0,5,1,6,2,4], # horizontal (last move is middle of line)
				[0,1,1,2,3,3,3,4,3,2,2],# upper right line
				[3,3,3,4,5,2,2,2,2,6,4],# upper left line
				]

		for k in range(len(test_moves)):
			b = bitboard.BitBoard(4,7,6)
			p = b.FIRST
			for move in test_moves[k]:
				c = move
				b.update(p,c)
				p = b.FIRST if p == b.SECOND else b.SECOND
			b.display()
			row = ((b.POS >> (3*c)) & 7)-1
			res = b.check(row ,test_moves[k][-1],b.FIRST)
			self.assertTrue(res, 'failed in k= '+str(k)+'('+str(row)+','+str(test_moves[k][-1])+')')

	def test_draw_check(self):
		b = self.bb
		p = b.FIRST
		for r in range(b.HEIGHT):
			for c in range(b.WIDTH):
				b.update(p,c)
				p = b.FIRST if p==b.SECOND else b.SECOND
		b.display()
		self.assertTrue(b.checkDraw(), 'Failed in checkDraw function')

if __name__ == '__main__':
	unittest.main()
