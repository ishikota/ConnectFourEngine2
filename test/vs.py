import os
import sys
PARENT_PATH = os.getcwd()[:-4]
sys.path.append(PARENT_PATH+'src/ui')
sys.path.append(PARENT_PATH+'src/strategy')
import bitboard
import iterative_deepening
import iterative_deepening2
import id_move_ordering
import id_tt
import pdb
import time
import game_simulator

b = bitboard.BitBoard(4,7,6)
simulator = game_simulator.GameSimulator()

#############################################################
# set first player as name s1
s1_name = 'IterativeDeepening'
#s1 = iterative_deepening.IterativeDeepening(b.FIRST)
#s1 = id_move_ordering.IterativeDeepening(b.FIRST)
s1 = id_tt.IterativeDeepening(b.FIRST)
s1.setParam(s1.TIME_LIMIT_MODE, 2)
s1.D = True

# set second player as name s2
s2_name = 'IterativeDeepening'
#s2 = iterative_deepening.IterativeDeepening(b.SECOND)
#s2 = id_move_ordering.IterativeDeepening(b.SECOND)
s2 = id_tt.IterativeDeepening(b.SECOND)
s2.setParam(s2.TIME_LIMIT_MODE, 2)
s2.D = True

# set simulation parameter
N = 1 # the number of times to play match
simulator.D = True # if True then display game progress
#############################################################

# 0 : DRAW, 1 : WIN, 2: LOSE
results = [0 for i in range(3)]
for i in range(N):
	print 'THE '+str(i+1)+' th GAME NOW ...'
	result = simulator.play(s1, s2)
	results[result] += 1
	if result == 0: print 'DRAW'
	elif result == 1: print 'FIRST PLAYER WIN'
	else: print 'FIRST PLAYER LOSE'

print ''
print '******************* TEST RESULT *******************'
print s1_name +' VS '+s2_name
print s1_name+' win against '+s2_name+' : '+str(results[1])
print s1_name+' lose against '+s2_name+' : '+str(results[2])
print s1_name+' draw against '+s2_name+' : '+str(results[0])
print '***************************************************'
print ''
