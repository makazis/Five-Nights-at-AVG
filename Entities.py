from math import *
from random import *
import pygame
Tcount=1
class Teacher:
    def __init__(self,tips=-1):
        self.tips=tips
        if self.tips==-1:
            self.tips=randint(1,Tcount)
        if self.tips==1: #Doug Dave Leepin
            self.sprite=None
            self.x=0
            self.y=0
            self.angle=0
            self.graphs=[]
