class BitBoard:
	
	def __init__(self, connect_k, width, height):
		self.CONNECT_K = connect_k
		self.WIDTH = width
		self.HEIGHT = height
		self.FB = 0
		self.SB = 0
		self.POS = 0 # represents position by 3bit*WIDTH(most right 3-bit represents next row of column 0) 
		self.FIRST = 2
		self.SECOND = 4
		# variable for check function
		self.R_MASK  = int('111111011111101111110111111011111101111110', 2)
		self.L_MASK  = int('011111101111110111111011111101111110111111', 2)
		self.UR_MASK = int('111111011111101111110111111011111111111111', 2)
		self.LL_MASK = int('111111111111110111111011111101111110111111', 2)
		self.UL_MASK = int('011111101111110111111011111101111110111111', 2)
		self.LR_MASK = int('111111011111101111110111111011111101111110', 2)


	def display(self):
		line = [' ' for i in range(self.HEIGHT)]
		for row in range(self.HEIGHT):
			for col in range(self.WIDTH):
				line[row] += 'O' if (self.FB>>(row*self.WIDTH+col)&1)==1 else 'X' if (self.SB>>(row*self.WIDTH+col)&1)==1 else '-'
				line[row] += ' '
		#print 
		print ''
		for i in reversed(range(self.HEIGHT)): print line[i]
		print ' 1 2 3 4 5 6 7'
	
	def getRow(self, col):
		return (self.POS >> (col*3)) & 7 # retrieve 3-bit which represents next row of col

	def update(self, player, col):
		row = self.getRow(col)
		if player == self.FIRST:
			self.FB = self.FB | (1<<(row*self.WIDTH + col))
		else:
			self.SB = self.SB | (1<<(row*self.WIDTH + col))
		self.POS += 1<< (col*3)

	def refresh(self):
		self.FB = 0
		self.SB = 0
		self.POS = 0 

	def check(self, row, col, player):
		b = self.FB if player == self.FIRST else self.SB
		m = 1<<(row*self.WIDTH + col) # bit position to make a move
		# check 7 direction (except upper direction)
		# check order is 
		# horizontal(right->left), upper right(upper right->lower left), upper left(upper left->lower right), vertival(lower)
		count = 1
		for k in range(7):
			mask = self.transfer(m,k)
			for i in range(3):
				if mask==0 or mask&b==0: break
				count += 1
				mask = self.transfer(mask, k)
			if (k==1 or k==3 or k==5 or k==6):
				if count >= 4: return True
				else: count = 1
		
		return False

	def transfer(self,m,d):
		if d == 0: return (m<<1) & self.R_MASK # right direction
		if d == 1: return (m>>1) & self.L_MASK # left direction
		#if d == 2: return (m<<self.WIDTH) # upper direction
		if d == 2: return (m<<(self.WIDTH+1)) & self.UR_MASK # upper right
		if d == 3: return (m>>(self.WIDTH+1)) & self.LL_MASK # lower left
		if d == 4: return (m<<(self.WIDTH-1)) & self.UL_MASK # upper left
		if d == 5: return (m>>(self.WIDTH-1)) & self.LR_MASK # lower right
		if d == 6: return (m>>self.WIDTH) # lower direction

	def checkDraw(self):
		return (self.FB | self.SB)^((1<<42)-1) == 0
