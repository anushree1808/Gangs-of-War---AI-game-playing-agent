from numpy import array
from numpy import empty
from collections import deque
import copy

class homework:
    def __init__(self):
        self.content = []
        self.N = 0
        self.cellval = empty([0,0])#creates empty array
        self.board = empty([0,0])
        self.mode = ""
        self.player = ""
        self.posN = deque()
        self.depth = 0
        self.score = 0
        
    def readinput(self,filename):
        fo = open(filename,'rU')
        content = []
        with fo as f:
            self.content = [line.strip() for line in f.readlines()]
        self.N = int(self.content[0])
        self.mode = self.content[1]
        self.player = self.content[2]
        self.depth = int(self.content[3])
        end1 = 4+self.N
        end2 = end1+self.N
        for i in range(4,end1):
            self.content[i] = [int(j) for j in self.content[i].split(" ")]
        for i in range(end1,end2):
            self.content[i] = list(self.content[i])
        self.cellval = array(self.content[4:end1])
        self.board = array(self.content[end1:end2])
        self.curstate()
        #self.mode = "COMPETITION"
        #print self.depth
        return self.mode

    def curstate(self):
        for i in range (self.N):
            for j in range(self.N):
                if self.board[i][j] == '.':
                    self.posN.append((i,j))
                elif self.board[i][j] == self.player:
                    self.score += self.cellval[i][j]
                else :
                    self.score -= self.cellval[i][j]

    def raid(self,bcopy,i,j,pla,opp,score):
        l = self.N
        bcopy[i][j]=pla
        delta = 0
        
        if (i>0 and bcopy[i-1][j] == opp ):
            bcopy[i-1][j] = pla
            delta += 2*self.cellval[i-1][j]
        if (i<l-1 and bcopy[i+1][j] == opp):
            bcopy[i+1][j] = pla
            delta += 2*self.cellval[i+1][j]
        if (j>0 and bcopy[i][j-1] == opp):
            bcopy[i][j-1] = pla
            delta += 2*self.cellval[i][j-1]
        if (j<l-1 and bcopy[i][j+1] == opp):
            bcopy[i][j+1] = pla
            delta += 2*self.cellval[i][j+1]
        delta += self.cellval[i][j]
        
        if pla == self.player :
            return score + delta
        else:
            return score - delta
    
    def nextpos(self,board):
        n = self.N
        for i in range(n):
            for j in range(n):
                if board[i][j]=='.':
                    yield i,j

    def generatesuccessors(self,board,player,score):
        bcopy = copy.deepcopy(board)
        s = score
        
        if player == 'X':
            pla = 'X'
            opp = 'O'
        else:
            pla = 'O'
            opp = 'X'
            
        np = self.nextpos(bcopy)
        #print np
        for pos in np :
            #print pos
            bcopy[pos[0]][pos[1]] = pla
            if pla == self.player:
                score += self.cellval[pos[0]][pos[1]]
            else :
                score -= self.cellval[pos[0]][pos[1]]
            yield 'Stake',pos,bcopy,score
            bcopy = copy.deepcopy(board)
            score = s

        score = s
        l = self.N
        np = self.nextpos(board)
        for pos in np :
            i = pos[0]
            j = pos[1]
            p = False
            o = False
            if (i>0 and bcopy[i-1][j] == pla) or (i<l-1 and bcopy[i+1][j] == pla) or (j>0 and bcopy[i][j-1] == pla) or (j<l-1 and bcopy[i][j+1] == pla):
                p = True
            if (i>0 and bcopy[i-1][j] == opp)or (i<l-1 and bcopy[i+1][j] == opp) or (j>0 and bcopy[i][j-1] == opp) or (j<l-1 and bcopy[i][j+1] == opp):
                o = True
            if p and o :
                score = self.raid(bcopy,i,j,pla,opp,score)
                yield 'Raid',pos,bcopy,score
                bcopy = copy.deepcopy(board)
                score = s

    def evaluate(self,board):
        x_val = 0
        o_val = 0
        score = 0
        n = self.N
        cellval = self.cellval
        for i in range(n):
            for j in range(n):
                if board[i][j] == 'X':
                    x_val += cellval[i][j]
                elif board[i][j] == 'O':
                    o_val += cellval[i][j]
        if self.player == 'X':
            return x_val-o_val
        else :
            return o_val-x_val

    def minvalue(self,succ,depth,cur_player):
        if depth == 1:
            return succ[3]
        v = float("inf")
        depth -= 1
        if cur_player =='X':
            next_player = 'O'
        else :
            next_player = 'X'
        move = False
        successors = self.generatesuccessors(succ[2],next_player,succ[3])
        for suc in successors:
            move = True
            v = min(v,self.maxvalue(suc,depth,next_player))
        if move :
            return v
        else :
            return succ[3]

    def maxvalue(self,succ,depth,cur_player):
        if depth == 1 :
            return succ[3]
        v = float("-inf")
        depth -= 1
        if cur_player =='X':
            next_player = 'O'
        else :
            next_player = 'X'
        move = False
        successors = self.generatesuccessors(succ[2],next_player,succ[3])
        for suc in successors:
            move = True
            v = max(v,self.minvalue(suc,depth,next_player))
        if move :
            return v
        else :
            return succ[3]
                
    def MINIMAX(self):
        print "Minimax"
        successors = self.generatesuccessors(self.board,self.player,self.score)
        maxim = tuple()
        m_score = float("-inf")
        for succ in successors :
            score = self.minvalue(succ,self.depth,self.player)
            if score > m_score :
                maxim = succ
                m_score = score

        print m_score
        print maxim
        self.writeoutput(maxim)

    def minvalue_ab(self,succ,depth,cur_player,alpha,beta):
        if depth == 1 :
            return succ[3]
        v = float("inf")
        depth -= 1
        if cur_player =='X':
            next_player = 'O'
        else :
            next_player = 'X'
        move = False
        successors = self.generatesuccessors(succ[2],next_player,succ[3])
        for suc in successors:
            move = True
            v = min(v,self.maxvalue_ab(suc,depth,next_player,alpha,beta))
            if v <= alpha:
                return v
            beta = min(v,beta)
        if move :
            return v
        else :
            return succ[3]

    def maxvalue_ab(self,succ,depth,cur_player,alpha,beta):
        if depth == 1:
            #return  self.evaluate(succ[2])
            return succ[3]
        v = float("-inf")
        depth -= 1
        if cur_player =='X':
            next_player = 'O'
        else :
            next_player = 'X'
        move = False
        successors = self.generatesuccessors(succ[2],next_player,succ[3])
        for suc in successors:
            move = True
            v = max(v,self.minvalue_ab(suc,depth,next_player,alpha,beta))
            if v>=beta:
                return v
            alpha = max(alpha,v)
        if move :
            return v
        else :
            return succ[3]

    def ALPHABETA(self):
        print "AlphaBeta"
        #print self.depth
        successors = self.generatesuccessors(self.board,self.player,self.score)
        maxim = tuple()
        m_score = float("-inf")
        for succ in successors :
            score = self.minvalue_ab(succ,self.depth,self.player,float("-inf"),float("inf"))
            if score > m_score :
                maxim = succ
                m_score = score

        #print m_score
        #print maxim
        self.writeoutput(maxim)

    def COMPETITION(self):
        print "Competition"
        if self. N > 18:
            self.depth = 1
        elif self.N > 12 :
            self.depth = 2
        elif self.N > 6:
            self.depth = 3
        else:
            self.depth = 4
        self.ALPHABETA()

    def writeoutput(self,maxim):
        cord = maxim[1]
        pos = chr(ord('A')+cord[1])+str(cord[0]+1)
        fname = "output.txt"
        fo = open(fname, 'w')
        outlist = []
        outlist.append(pos+" "+maxim[0]+"\n")
        for i in maxim[2]:
            st = ("").join(i)+"\n"
            outlist.append(st)
        print "\n"
        print outlist
        fo.writelines(outlist)
        fo.close()

obj = homework()
#mode = obj.readinput("TC/Test10/input.txt")
mode = obj.readinput("input.txt")
res = getattr(obj,mode)()

