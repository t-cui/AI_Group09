# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from sensed_world import SensedWorld
from colorama import Fore, Back

Wvalues=[]
class TestCharacter(CharacterEntity):

    def do(self, wrld):
        # Your code here
        # action: up, down, left, right, leftup, leftdown, rightup, rightdown, boom
        if(Wvalues[0] != []):
            Wvalues = [10, -100, -100, 1000, -10, -100]
        sWrld= SensedWorld.from_world(wrld)
        (newWorld, events) = sWrld.next()
        currscore = sWrld.scores["me"]
        nextscore = newWorld.scores["me"]
        currx=self.x
        curry=self.y
        nextx=[]
        nexty=[]
        # nextx_up, nexty_up = self.nextstep(wrld, currx, curry, "up")
        # nextx_down, nexty_down =  self.nextstep(wrld, currx, curry, "down")
        # nextx_left, nexty_left =  self.nextstep(wrld, currx, curry, "left")
        # nextx_right, nexty_right =  self.nextstep(wrld, currx, curry, "right")
        # nextx_leftup, nexty_leftup =  self.nextstep(wrld, currx, curry, "leftup")
        # nextx_leftdown, nexty_leftdown =  self.nextstep(wrld, currx, curry, "leftdown")
        # nextx_rightdown, nexty_rightdown =  self.nextstep(wrld, currx, curry, "rightdown")
        # nextx_rightup, nexty_rightup =  self.nextstep(wrld, currx, curry, "rightup")
        direction= ["up", "down", "left", "right", "leftup", "leftdown", "rightup", "rightdown"]
        for i in range(len(direction)):
            nextdirx, nextdiry = self.nextstep(wrld, currx, curry, direction[i])
            nextx.append(nextdirx)
            nexty.append(nextdiry)
        currQval = self.Qvalue(wrld, Wvalues[0], Wvalues[1], Wvalues[2], Wvalues[3], Wvalues[4], Wvalues[5], currx, curry)
        BestQ=-99999
        Bestxy=(-99,-99)
        Bestmove=(-99,-99)
        for j in range(len(nextx)):
            Qdirval=self.Qvalue(wrld, Wvalues[0], Wvalues[1], Wvalues[2], Wvalues[3], Wvalues[4], Wvalues[5], nextx[j], nexty[j])
            if (Qdirval > BestQ):
                BestQ = Qdirval
                Bestxy=(nextx[j], nexty[j])
        Bestmove=(Bestxy[0]-self.x, Bestxy[1]-self.y)
        reward = nextscore - currscore 
        delta = reward + BestQ - currQval
        for k in range(len(Wvalues)):
            Wvalues[k] = Wvalues[k] + delta*0.4*BestQ
        self.move(Bestmove[0], Bestmove[1])

    def nextstep(self, wrld, currx, curry, dirt):
        nextx=currx
        nexty=curry
        if (dirt == "right"):
            if(currx+1<wrld.width()):
                nextx=nextx+1
                return nextx, nexty
        if(dirt=="left"):
            if(currx-1>=0):
                nextx=nextx-1
                return nextx, nexty
        if(dirt=="up"):
            if(curry-1>=0):
                nexty=nexty-1
                return nextx, nexty 
        if(dirt=="down"):
            if(curry+1<wrld.height()):
                nexty=nexty+1
                return nextx, nexty 
        if(dirt=="leftup"):
            if(currx-1>=0):
                nextx=nextx-1
            if(curry-1>=0):
                nexty=nexty-1
            return nextx, nexty   
        if(dirt=="leftdown"):
            if(currx-1>=0):
                nextx=nextx-1
            if(curry+1<wrld.height()):
                nexty=nexty+1
            return nextx, nexty
        if(dirt == "rightup"):
            if(currx+1<wrld.width()):
                nextx=nextx+1
            if(curry-1>=0):
                nexty=nexty-1
            return nextx, nexty
                               
    def Qvalue (self, wrld, Wa, Wb, Wc, Wd, We, Wf, currx, curry):
        # features: destory a wall, monster, monster, exit, bomb, explosion 
        newWall = self.FindCloseWall(wrld, currx, curry)
        Fa=0
        Fe=0
        Ff=0
        if(newWall!=(-1,-1)):
            Fa = self.FindManhDist(newWall[0], newWall[1], currx, curry)
        mx, my = self.FindMons(wrld)
        Fb = self.FindManhDist(mx[0],my[0], currx, curry)
        Fc = self.FindManhDist(mx[1],my[1],  currx, curry)
        dx, dy = self.FindExit(wrld)
        Fd = self.FindManhDist(dx, dy, currx, curry)
        newBomb = self.FindCloseBomb(wrld, currx, curry)
        if(newBomb!=(-1,-1)):
            Fe = self.FindManhDist(newBomb[0], newBomb[1], currx, curry)
        newExplo = self.FindCloseExplosion(wrld, currx, curry)
        if(newExplo!=(-1,-1)):
            Ff = self.FindManhDist(newExplo[0], newExplo[1], currx, curry)
        Q = Wa*Fa + Wb*Fb + Wc*Fc + Wd*Fd + We*Fe + Wf*Ff
        return Q

    def FindExit(self,wrld):
        for x in range (wrld.width()):
            for y in range (wrld.height()):
                if(wrld.exit_at(x,y)):
                    return x,y
        return -1,-1    
    
    def FindCloseBomb(self, wrld, currx, curry):
        p = []
        old=9999
        newBomb=(-1,-1)
        for x in range (wrld.width()):
            for y in range (wrld.height()):
                if(wrld.bomb_at(x,y)):
                    p.append((x,y))
        for i in p:
            newdis = abs(i[0]-currx)+abs(i[1]+curry)
            if(old>newdis):
                old=newdis
                newBomb=(i[0], i[1])
        return newBomb

    def FindMons(self, wrld):
        lx = []
        ly = []
        for x in wrld.width():
            for y in wrld.height():
                if(wrld.monsters_at(x,y)!=[]):
                    lx.append(x)
                    ly.append(y)
        return lx,ly

    def FindCloseWall(self, wrld, currx, curry):
        p = []
        old=9999
        newWall=(-1,-1)
        for x in range (wrld.width()):
            for y in range (wrld.height()):
                if(wrld.wall_at(x,y)):
                    p.append((x,y))
        for i in p:
            newdis = abs(i[0]-currx)+abs(i[1]+curry)
            if(old>newdis):
                old=newdis
                newWall=(i[0], i[1])
        return newWall

    def FindCloseExplosion(self, wrld, currx, curry):
        p = []
        old=9999
        newExplo=(-1,-1)
        for x in range (wrld.width()):
            for y in range (wrld.height()):
                if(wrld.explosion_at(x,y)):
                    p.append((x,y))
        for i in p:
            newdis = abs(i[0]-currx)+abs(i[1]+curry)
            if(old>newdis):
                old=newdis
                newExplo=(i[0], i[1])
        return newExplo

    def FindManhDist(self, x , y, currx, curry):
        dx = x-currx
        dy = y-curry
        dist = abs(dx) + abs(dy)
        return dist

    # def checkavabile(self, wrld):
    #     print("checkavabile \n")
    #     w = SensedWorld.from_world(wrld)
    #     px=self.x
    #     py=self.y
    #     print(px,py, "\n")
    #     avail = [0,0,0,0]
    #     print(w.empty_at(px+1, py), "right\n")
    #     if(w.empty_at(px+1, py) is True):
    #         avail[3]=1
    #     if(w.empty_at(px-1, py) is True):
    #         avail[2]=1
    #     if(w.empty_at(px, py+1) is True):
    #         avail[1]=1
    #     if(w.empty_at(px, py-1) is True):
    #         avail[0]=1     

    #     return avail