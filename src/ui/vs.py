import os
import sys
PARENT_PATH = os.getcwd()[:-2]
sys.path.append(PARENT_PATH+'strategy')
import pdb

import bitboard
import game_manager
import human
import random_strategy
import id_move_ordering
import base_mcts

# flg constant for getStrategy(flg, me) method
MINI_MAX = 1
UCT_MCTS = 2
TUNED_MCTS = 3

def getStrategy(flg, me):
	if flg == MINI_MAX: return id_move_ordering.IterativeDeepening(me)
	if flg == UCT_MCTS: return base_mcts.BaseMCTS(me)
	return random_strategy.RandomStrategy(me)

def checkFinishFlg(flg):
	if flg == -1:
		print '> FINISH THE GAME'
		return True
	else:
		return False

# initialize variables
GM = game_manager.GameManager()
board = bitboard.BitBoard(4,7,6)

# show menu and initialize player
p1, p2 = 0, 0
GM.introduction()

# choose first player
if GM.askPlayerIsCPU('FIRST PLAYER'):
	flg_strategy = GM.askCPUStrategy()
	p1 = getStrategy(flg_strategy, board.FIRST)
	#GM.askStrategyParameter(flg_strategy, p1)
	GM.askCPUThinkingTime(flg_strategy, p1)
else:
	p1 = human.Human(board.FIRST)

# choose second player
if GM.askPlayerIsCPU('SECOND PLAYER'):
	flg_strategy = GM.askCPUStrategy()
	p2 = getStrategy(flg_strategy, board.SECOND)
	#GM.askStrategyParameter(flg_strategy, p2)
	GM.askCPUThinkingTime(flg_strategy, p2)
else:
	p2 = human.Human(board.SECOND)
#################################################################################
# If you want to read board state from in.txt file, change if_read_board to True.
if_read_board = False
read_file_name = 'in.txt'
# flg to run strategy in debug mode
p1.D = True
p2.D = True
#################################################################################
switched_player = False
if if_read_board:
	switched_player = GM.readBoard(read_file_name, board)
	print 'Readed Board state !!';print ''
	if switched_player:
		temp = p1
		p1 = p2
		p2 = temp


# Start Connect Four !!
board.display()
print '> START THE GAME !!'
while True:
	# first player turn
	col = p1.think(board)
	if checkFinishFlg(col): break
	board.update(p1.ME, col)
	board.display()
	if board.check(board.getRow(col)-1, col, p1.ME):
		p = 'FIRST' if not switched_player else 'SECOND'
		print '\n> '+p+' PLAYER WIN !!\n'
		break
	# second player turn
	col = p2.think(board)
	if checkFinishFlg(col): break
	board.update(p2.ME, col)
	board.display()
	if board.check(board.getRow(col)-1, col, p2.ME):
		p = 'SECOND' if not switched_player else 'FIRST'
		print '\n> '+p+' PLAYER WIN !!\n'
		break
	
	if board.checkDraw():
		print '\nDraw!!\n'
		break

