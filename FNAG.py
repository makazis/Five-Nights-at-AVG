from math import *
from random import *
import pygame
pygame.init()
win=pygame.display.set_mode((1800,900))
S1=pygame.Surface((200,100))
S2=pygame.image.load("MAP.xcf")
run=True
font=pygame.font.SysFont("papyrus",20)
Sags=pygame.Surface((1,100))
Sags.set_colorkey((0,0,0))
Sags.set_alpha(100)
Glassground=pygame.Surface((200,100))
Glassground.set_alpha(1)
Glassground.fill((0,228,255))
Map=[]
light_mode=True
for i in range(50):
    line=[]
    for i1 in range(50):
        if S2.get_at((i,i1))==(255,255,255):
            line.append(0)
        else:
            line.append(1)
    Map.append(line)
x=84
y=897
angle=0
bounced=False
btimer=0
sprint_timer=0
#Inventory Item indexes and descriptions
# 0. Flashlight, (power)
# 
#
#
#
inventory=[[0,3000]]
hand_item=0
flashlight_on=False
pygame.mouse.set_visible(False)
t1=False
alive=True
death_reason="Undefined"
hp=100
while run and alive and hp>0:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    keys=pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]: run=False
    mouse_rel=pygame.mouse.get_pos()
    mouse_down=pygame.mouse.get_pressed()
    pygame.mouse.set_pos((900,450))
    angle+=(mouse_rel[0]-900)/100
    S1.fill((0,0,0))
    win.blit(pygame.transform.scale(S2,(900,900)),(900,0))
    sec_rays=[]
    for i in range(200):
        angle2=angle+i/100-1
        distance=2
        walkdistance=2
        ray_x=x
        ray_y=y
        rayspeed=[cos(angle2)/2,sin(angle2)/2]
        color=(255,255,255)
        difrakcija=4
        cbonus=[0,0,0]
        dislimit=102
        if 50<i<150 and flashlight_on:
            dislimit=204
        while color in [(255,255,255),(0,228,255),(0,0,1),(0,0,2),(0,0,3),(0,0,4)] and distance<dislimit:
            try:
                color=S2.get_at((round(ray_x),round(ray_y)))
            except:
                break
            if color==(0,228,255):
                sec_rays.append([i,40-150/distance,(0,228,255)])
                rayspeed=[-i for i in rayspeed]
            if color==(0,0,1):
                ray_x+=38
                ray_y+=14
            if color==(0,0,2):
                ray_x-=38
                ray_y-=14
            if color==(0,0,3):
                ray_x-=4
                ray_y-=209
                rayspeed=[-i for i in rayspeed]
            if color==(0,0,4):
                ray_x+=2
                ray_y+=209
                rayspeed=[-i for i in rayspeed]
            ray_x+=rayspeed[0]
            ray_y+=rayspeed[1]
            distance+=1
            walkdistance+=1
        if color==(255,255,255):
            color=(0,0,0)
        if i==100 and walkdistance>4:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                x+=cos(angle)*0.05
                y+=sin(angle)*0.05
            if keys[pygame.K_SPACE] and sprint_timer<1000:
                x+=cos(angle)*0.15
                y+=sin(angle)*0.15
                sprint_timer+=3
            elif sprint_timer>0:
                sprint_timer-=1
        elif walkdistance<=4:
            x-=cos(angle)*0.05
            y-=sin(angle)*0.05
        distance=40-150/distance
        color=[min(255,max(0,color[i]+cbonus[i])) for i in range(3)]
        try:
            if light_mode:
                if dislimit==204:
                    disbonus=abs(100-i)/24
                    pygame.draw.line(S1,(max(color[0]-distance*(1.5+disbonus),0),max(color[1]-distance*(1.5+disbonus),0),max(color[2]-distance*(1.5+disbonus),0)),(i,distance),(i,100-distance))
                else:
                    pygame.draw.line(S1,(max(color[0]-distance*3.5,0),max(color[1]-distance*3.5,0),max(color[2]-distance*3.5,0)),(i,distance),(i,100-distance))
            else:
                if dislimit==204:
                    disbonus=abs(100-i)/24
                    pygame.draw.line(S1,(max(color[0]-distance*(3.5+disbonus),0),max(color[1]-distance*(3.5+disbonus),0),max(color[2]-distance*(3.5+disbonus),0)),(i,distance),(i,100-distance))
                else:
                    pygame.draw.line(S1,(max(color[0]-distance*5.5,0),max(color[1]-distance*5.5,0),max(color[2]-distance*5.5,0)),(i,distance),(i,100-distance))
        except:
            pass
    for i in range(len(sec_rays)):
        c2=(min(255,max(sec_rays[i][2][0]-sec_rays[i][1]*5,0)),min(255,max(sec_rays[i][2][1]-sec_rays[i][1]*5,0)),min(255,max(sec_rays[i][2][2]-sec_rays[i][1]*5,0)))
        Sags.fill((0,0,0))
        Sags.set_alpha(int(max(0,30-sec_rays[i][1]))*6)
        pygame.draw.line(Sags,c2,(0,sec_rays[i][1]),(0,100-sec_rays[i][1]))
        S1.blit(Sags,(sec_rays[i][0],0))
    pcolor=S2.get_at((round(x),round(y)))
    if pcolor==(0,228,255):
        angle+=pi
        bounced=not bounced
        btimer=0
        t1=True
    elif pcolor==(0,0,1):
        x+=38
        y+=14
        t1=True
    elif pcolor==(0,0,2):
        x-=38
        y-=14
        t1=True
    elif pcolor==(0,0,3):
        x-=4
        angle+=pi
        y-=209
        t1=True
    elif pcolor==(0,0,4):
        x+=2
        angle+=pi
        y+=209
        t1=True
    elif t1:
        t1=False
    else:
        if bounced:
            btimer+=1
            if btimer>800:
                alive=False
                death_reason="Mirror"
            Glassground.set_alpha(int(btimer/4))
            S1.blit(Glassground,(0,0))
        true_x=(x+0.5)*18
        true_y=(y+0.5)*18
        if len(inventory)>0:
            item=inventory[hand_item]
            if item[0]==0: #Flashlight
                if mouse_down[0]:
                    item[1]-=1
                    flashlight_on=True
                else:
                    flashlight_on=False
                if item[1]<=0:
                    inventory.remove(item)
                    flashlight_on=False
                pygame.draw.rect(S1,(255,255,0),(198,25,1,50*item[1]/3000))
        pygame.draw.rect(S1,(255,0,255),(199,25,2,50-50*sprint_timer/1000))
        pygame.draw.rect(S1,(0,255,255),(199,75,2,25-25*btimer/800))
        
        pygame.draw.circle(win,(255,0,0),(true_x+900,true_y),5)
        win.blit(pygame.transform.scale(S1,(1800,900)),(0,0))
        pygame.display.update()
if alive==False:
    if death_reason=="Mirror":
        S1.blit(font.render("Tu tiki Spogulots",1,(0,114,125)),(30,30))
        win.blit(pygame.transform.scale(S1,(1800,900)),(0,0))
    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        pygame.display.update()
pygame.quit()
