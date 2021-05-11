botName='dymieu-defbot'

import json
import numpy as np
from random import choices

def calculateMove(gameState):
    g=GameState(gameState["Board"],0)
    a=Agent()
    dropColumn=a.getAction(g)
    return {"Column": dropColumn}

def isColumnFullX(dropColumn,board):
    if len([x[dropColumn] for x in board if x[dropColumn] == -1]) > 0:
        return False
    return True
    
class Agent:
    def __init__(self, depth='1'):
        self.index = 0  # Pacman is always agent index 0
        self.depth = int(depth)
        
    def evaluationFunction(self,gameState):
        board=np.array(gameState.Board)
        newboard=(board==1).astype(np.int)+(np.abs(board)>0).astype(np.int)
        m,n=newboard.shape
        score1=0
        for i in range(m):
            for j in range(n):
                if newboard[i,j]==2:
                    stepscore=lineSearch(newboard,i,j)
                    if stepscore>=6:
                        score1+=stepscore**2
        newboard=(board==0).astype(np.int)+(board<=0).astype(np.int)             
        score2=0
        for i in range(m):
            for j in range(n):
                if newboard[i,j]==2:
                    stepscore=lineSearch(newboard,i,j)
                    if stepscore>=5:
                        score2+=stepscore
        newboard=(board==0)-(board==1)
        addition=np.sum(newboard,axis=0)
        return addition.dot(np.array([1,2,5,10,5,2,1]))-10*score1+10*score2
        
        
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        agents=2
        alpha=-999999
        beta=999999
        def MAX_VALUE(state,depth,agent,alpha,beta):
            if state.isWin():
                return [-100000,"Stop"]
            if depth==self.depth*agents:
                return [self.evaluationFunction(state),'Stop']
            v=-999999
            a="Stop"
            if len(state.getLegalActions())==0:
                return [0,'Stop']
            for i in state.getLegalActions():
                v1=MIN_VALUE(state.generateSuccessor(1-agent,i),depth+1,1,alpha,beta)
                if(v<v1):
                    v=v1
                    a=i
                if(v>beta):
                    return [v,a]
                alpha=max(v,alpha)
            return [v,a]

        def MIN_VALUE(state,depth,agent,alpha,beta):
            if state.isWin() :
                return 100000
            v=999999
            if len(state.getLegalActions())==0:
                return 0
            for i in state.getLegalActions():
                v=min(v, MAX_VALUE(state.generateSuccessor(1-agent, i), depth+1,0,alpha,beta)[0])
                if (v<alpha):
                    return v
                beta=min(v,beta)
            return v
        for i in gameState.getLegalActions():
            if gameState.generateSuccessor(0,i).isWin() or gameState.generateSuccessor(1,i).isWin():
                return i[1]
        return MAX_VALUE(gameState,0,0,alpha,beta)[1][1]

def drop(board,Column):
    if board[-1][Column]==-1:
        return len(board)-1
    for x in range(len(board)-1):
        if board[x+1][Column]!=-1:
            return x
            
def deepcopy(board):
    n=len(board)
    a=list(range(n))
    for i in range(n):
        a[i]=board[i].copy()
    return a
            
class GameState:
    def __init__(self,board,mover,lastdrop =None):
        self.Board=deepcopy(board)
        self.Mover=mover
        self.LastDrop=lastdrop
        
    def getLegalActions(self):
        emptyGrid=[]
        board=self.Board
        n=len(board[0])
        for i in range(n):
            if not isColumnFullX(i,board):
                emptyGrid.append((drop(board,i),i))
        return emptyGrid
        
    def generateSuccessor(self,agentIndex,action):
        g=GameState(self.Board,self.Mover,action)
        g.Board[action[0]][action[1]]=g.Mover
        g.Mover=agentIndex
        return g
        
    def isWin(self):
        board=(np.array(deepcopy(self.Board))==1-self.Mover)
        if self.LastDrop==None:
            return False
        x,y=self.LastDrop
        if lineSearch(board,x,y)>=4:
            return True
        else:
            return False
            

def lineSearch(board,x,y):
    m,n=board.shape
    score=[0,0,0,0]
    #列
    l,r=0,0
    while True:
        if board[x+r,y]>0:
            score[0]+=board[x+r,y]
            r+=1
        else:
            break
        if x+r==m:
            break
    while True:
        if board[x-l,y]>0:
            score[0]+=board[x-l,y]
            l+=1
        else:
            break
        if x-l==-1:
            break
    if l+r<5:
        score[0]=0
    #行
    l,r=0,0
    while True:
        if board[x,y+r]>0:
            score[1]+=board[x,y+r]
            r+=1
        else:
            break
        if y+r==n:
            break
    while True:
        if board[x,y-l]>0:
            score[1]+=board[x,y-l]
            l+=1
        else:
            break
        if y-l==-1:
            break
    if l+r<5:
        score[1]=0
    #左斜
    l,r=0,0
    while True:
        if board[x-r,y+r]>0:
            score[2]+=board[x-r,y+r]
            r+=1
        else:
            break
        if y+r==n or x-r==-1:
            break
    while True:
        if board[x+l,y-l]>0:
            score[2]+=board[x+l,y-l]
            l+=1
        else:
            break
        if y-l==-1 or x+l==m:
            break
    if l+r<5:
        score[2]=0
    #右斜
    l,r=0,0
    while True:
        if board[x+r,y+r]>0:
            score[3]+=board[x+r,y+r]
            r+=1
        else:
            break
        if y+r==n or x+r==m:
            break
    while True:
        if board[x-l,y-l]>0:
            score[3]+=board[x-l,y-l]
            l+=1
        else:
            break
        if y-l==-1 or x-l==-1:
            break
    if l+r<5:
        score[3]=0
    return max(score)-1
