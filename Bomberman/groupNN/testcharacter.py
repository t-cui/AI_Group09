# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from sensed_world import SensedWorld
from colorama import Fore, Back

class TestCharacter(CharacterEntity):

    def do(self, wrld):
        # Your code here
        # action: up, down, left, right, leftup, leftdown, rightup, rightdown, boom
        poss = self.checkavabile(wrld)
        ex,ey=self.FindExit(wrld)
        if poss[1] == 1:
            print(ex, ey)
            self.move(0,1)
        x=0
        while(x=0):
            currevents = wrld.events
            for i in currevents:
                if(i.tpe == 4):
                    x = 1
            

    def Qvalue (self, wrld, Wa, Wb, Wc, Wd, We):
        # features: destory a wall, monster, monster, exit, boom causes death
        newWall = self.FindCloseWall(wrld)
        if(newWall!=(-1,-1)):
            Fa = self.FindManhDist(newWall[0], newWall[1])
        else Fa=0
        mx, my = self.FindMons(wrld)
        Fb = self.FindManhDist(mx[0],my[0])
        Fc = self.FindManhDist(mx[1],my[1])
        dx, dy = self.FindExit(wrld)
        Fd = self.FindManhDist(dx, dy)
        newBomb = self.FindCloseBomb(wrld)
        if(newWall!=(-1,-1)):
            Fe = self.FindManhDist(newBomb[0], newBomb[1])
        else Fe=0
        Q = Wa*Fa + Wb*Fb + Wc*Fc + Wd*Fd + We*Fe + Wf*Ff
        return Q


    def FindExit(self,wrld):
        for x in range (wrld.width()):
            for y in range (wrld.height()):
                if(wrld.exit_at(x,y)):
                    return x,y
        return -1,-1    
    
    def FindCloseBomb(self, wrld):
        p = []
        old=9999
        newBomb=(-1,-1)
        for x in range (wrld.width()):
            for y in range (wrld.height()):
                if(wrld.bomb_at(x,y)):
                    p.append((x,y))
        for i in p:
            newdis = abs(i[0]-self.x)+abs(i[1]+self.y)
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

    def FindCloseWall(self, wrld):
        p = []
        old=9999
        newWall=(-1,-1)
        for x in range (wrld.width()):
            for y in range (wrld.height()):
                if(wrld.wall_at(x,y)):
                    p.append((x,y))
        for i in p:
            newdis = abs(i[0]-self.x)+abs(i[1]+self.y)
            if(old>newdis):
                old=newdis
                newWall=(i[0], i[1])
        return newWall

    def FindCloseExplosion(self, wrld):
        p = []
        old=9999
        newExplo=(-1,-1)
        for x in range (wrld.width()):
            for y in range (wrld.height()):
                if(wrld.explosion_at(x,y)):
                    p.append((x,y))
        for i in p:
            newdis = abs(i[0]-self.x)+abs(i[1]+self.y)
            if(old>newdis):
                old=newdis
                newExplo=(i[0], i[1])
        return newExplo

    def FindManhDist(self, x , y):
        dx = x-self.x
        dy = y-self.y
        dist = abs(dx) + abs(dy)
        return dist

    def checkavabile(self, wrld):
        print("checkavabile \n")
        w = SensedWorld.from_world(wrld)
        px=self.x
        py=self.y
        print(px,py, "\n")
        avail = [0,0,0,0]
        print(w.empty_at(px+1, py), "right\n")
        if(w.empty_at(px+1, py) is True):
            avail[3]=1
        if(w.empty_at(px-1, py) is True):
            avail[2]=1
        if(w.empty_at(px, py+1) is True):
            avail[1]=1
        if(w.empty_at(px, py-1) is True):
            avail[0]=1     

        return avail