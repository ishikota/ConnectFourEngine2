import subprocess
class GameManager:

	def __init__(self):
		pass

	def introduction(self):
		subprocess.call('clear')
		print ''
		print '--- WELCOM TO CONNECT FOUR ---'
		print ''
		print '> IF YOU WANNA QUIT THE GAME,'
		print '> INPUT 0 AS YOUR INPUT.'
		print ''

	def showMenu(self):
		subprocess.call('clear')
		print ''
		print '--- MENU ---'
		print ' 1 : START GAME'
		print ' 2 : SET BOARD'
		print 'INPUT > '
		while(True):
			try:
				c = int(raw_input())
			except:
				print '> INVALID INPUT'
				continue
			if c == 1 or 2:
				return c

	# Returns true if passed user should be computer player
	def askPlayerIsCPU(self, player_str):
		print '> '+player_str+' IS ...'
		print '  1: HUMAN'
		print '  2: COMPUTER'
		print 'INPUT > '
		while True:
			try:
				c = int(raw_input())
			except:
				print '> INVALID INPUT'
				continue
			if c == 1 or c==2: 
				return c == 2

	def askCPUStrategy(self):
		print '> WHAT STRATEGY DOES COMPUTER USE ?'
		print '  1: MiniMax (IterativeDeepening)'
		print '  2: Flat MonteCarloTreeSearch'
		#print '  3: Arranged MonteCarloTreeSearch'
		while True:
			print 'INPUT > '
			try:
				c = int(raw_input())
			except:
				print '> INVALID INPUT'
				continue
			if 1<=c<=3: 
				return c

	def askCPUThinkingTime(self, flg_strategy, strategy):
		time = 3
		print '> INPUT THINKING TIME OF COMPUTER PLAYER (UNIT IS SECOND) ...' 
		while True:
			print 'INPUT > '
			try:
				time = int(raw_input())
			except:
				print '> INVALID INPUT'
				continue
			break
		
		if flg_strategy == 1: # MiniMax
			strategy.setParam(strategy.TIME_LIMIT_MODE, time)
		elif flg_strategy == 2: # Flat MonteCarloTreeSearch
			strategy.MODE = strategy.TIME_LIMIT_MODE
			strategy.setParameter(time)
		elif flg_strategy == 3: # arranged MonteCarloTreeSearch
			strategy.setParameter(strategy.TIME_IMIT_MODE, time, 8)

	'''
	Ask user about each parameter for strategy of computer.
		flg_strategy : flg of strategy which is returned from askCPUStrategy method
		strategy	 : instance of Strategy class to set parameter
	'''
	def askStrategyParameter(self, flg_strategy, strategy):
		if flg_strategy == 1: # MiniMax
			print '> INPUT MAX DEPTH OF MINIMAX ([1,10] is recommended)...'
			while True:
				print 'INPUT > '
				try:
					c = int(raw_input())
				except:
					print '> INVALID INPUT'
					continue
				break
			strategy.setParam(strategy.DEPTH_LIMIT_MODE, c)
		elif flg_strategy == 2: # Flat MonteCarloTreeSearch
			print '>INPUT THE NUMBER OF PLAYOUT IN MONTE-CALRO-TREE-SEARCH.'
			while True:
				print 'INPUT > '
				try:
					c = int(raw_input())
				except:
					print '> INVALID INPUT'
					continue
				break
			strategy.setParameter(c)
		elif flg_strategy == 3: # arranged MonteCarloTreeSearch
			print '>INPUT THE NUMBER OF PLAYOUT IN MONTE-CALRO-TREE-SEARCH.'
			while True:
				print 'INPUT > '
				try:
					c = int(raw_input())
				except:
					print '> INVALID INPUT'
					continue
				break
			strategy.setParameter(strategy.MODE_PLAYOUT_NUM_LIMIT,c, 8)
			

	def getInput(self, player_name, board):
		p = 0
		print '--- TURN [ '+player_name+' ] ---'
		while(True):
			try:
				print 'INPUT > '
				try:
					p = raw_input()
					p = int(p)
					if p == 0:
					    print '> ARE YOU SURE TO QUIT THE GAME? (y/n)'
					    if raw_input() != 'y': continue
					elif p<0 or board.WIDTH<p:
					    raise self.OutOfRangeInputError, p
					elif board.getRow(p-1) == board.HEIGHT:
					    raise self.FullPieceError, p
				except ValueError:
					raise self.OutOfRangeInputError, p
			except (self.OutOfRangeInputError, self.FullPieceError),e:
				print e
			else:
				break
		return p-1

	class OutOfRangeInputError(Exception):
		def __init__(self, value):
			self.value = value
		def __str__(self):
			return '> INPUT('+str(self.value)+') IS INVALID INPUT.\n> INPUT COLUMN NUMBER 1~6'

	class FullPieceError(Exception):
		def __init__(self, value):
			self.value = value
		def __str__(self):
			return '> YOU CANNOT PUT YOUR PIECE ON COLUMN '+str(self.value)+'.'

	def readBoard(self, file_name, board):
	# read board state from in.txt file.
	# and check which player is next.
	# return board, is_next_player_CPU
		table = [[0 for j in range(board.WIDTH)] for i in range(board.HEIGHT)]
		count1, count2 = 0, 0
		f = open(file_name, 'r')

		board_info = f.readline()
		try:
			width, height = map(int, board_info.split())
			if width != board.WIDTH or height != board.HEIGHT:
				raise ValueError
		except ValueError:
			print '> READ FAILED'
			print '> This input doesn\'t match to your board size'
			print ''
			return False

		for row in range(board.HEIGHT):
			temp = f.readline()
			line = temp.split()
			for col in range(board.WIDTH):
				table[board.HEIGHT-1-row][col] = line[col]
				if line[col] == 'O': count1 += 1
				elif line[col] == 'X': count2 += 1

		for c in range(board.WIDTH):
			for r in range(board.HEIGHT):
				char = table[r][c]
				p = board.FIRST if char=='O' else board.SECOND if char=='X' else -1
				if p == -1: break
				board.update(p,c)

		return count1!=count2

