from numpy import array
from numpy import ndarray
from numpy import empty
import numpy
import random

def create(n,player,depth):
	board = empty([n,n])
	#pos = numpy.chararray([n,n])
	pos = empty([n,n])
	pos = pos.astype(dtype='S1')
	for i in range(n):
		for j in range(n):
			board[i][j] = random.randint(1,99)
			pos[i][j] = '.'
	board = board.astype(int)
	board = board.astype(dtype=str)
	
	#print board[n-2][1]
	#print board
	#print pos
	fname = "input6.txt"
	fo = open(fname, 'w')
	outlist = []
	outlist.append(str(n)+"\n"+"ALPHABETA"+"\n"+player+"\n"+str(depth)+"\n")
	for i in board:
		#print i
		st = (" ").join(i)+"\n"
		outlist.append(st)
	for i in pos:
		st = ("").join(i)+"\n"
		outlist.append(st)
	print outlist
	fo.writelines(outlist)
	fo.close()
#call create(board_size, player, depth)
create(26,'X',2)