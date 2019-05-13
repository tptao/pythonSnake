import pygame
import random
import tkinter as tk
from tkinter import messagebox

pygame.init()
W = 800
H = 600
windowsize = (W, H)
ROW = 60  # 把window分成6*8个grid
COL = 80

bgcolor = (255, 255, 0)
headcolor = (255,0,0)
bodycolor = (100, 20, 125)
foodcolor = (255, 0, 200)
tailcolor = (0,0,0)

dir='L'




class Point:
    def __init__(self,row,col):
        self.row = row
        self.col = col
    def copy_toL(self):
        return Point(row=self.row, col=self.col-1)

    def copy_toR(self):
        return Point(row=self.row, col=self.col+1)

    def copy_toU(self):
        return Point(row=self.row-1, col=self.col)

    def copy_toD(self):
        return Point(row=self.row+1,col=self.col)


food = Point(row=random.randint(0,ROW-1), col=random.randint(0,ROW-1))
snakesarry = [Point(row=random.randint(0,ROW-1), col=random.randint(0,ROW-1))]
head = snakesarry[0]

def rect(Point, color):
    cell_width = W / COL
    cell_height = H / ROW

    left = Point.col * cell_width
    top = Point.row * cell_height
    pygame.draw.rect(window, color,
                     (left, top, cell_width, cell_height) )

def paint_snake():
    for snake in snakesarry:
        rect(snake,bodycolor)
    rect(snakesarry[0],headcolor)
    #rect(snakesarry[-1],tailcolor) # tail=snakesarry[-1] 居然錯誤

def snamke_move():
    head=snakesarry[0]  # head在不断的动态刷新
    # 沿着蛇头移动
    if dir == 'L':
        snakesarry.insert(0, head.copy_toL())
    elif dir == 'R':
        snakesarry.insert(0, head.copy_toR())
    elif dir == 'U':
        snakesarry.insert(0, head.copy_toU())
    elif dir == 'D':
        snakesarry.insert(0, head.copy_toD())
    snakesarry.pop()




def event_listen():
    global dir
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            playing = False
            pygame.quit()  # shout down window
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_DOWN or event.key==pygame.K_s )and dir != 'U':
                dir='D'
            elif( event.key==pygame.K_UP or event.key==pygame.K_w )and dir != 'D':
                dir='U'
            elif (event.key == pygame.K_LEFT or event.key==pygame.K_a) and dir != 'R':
                dir='L'
            elif (event.key==pygame.K_RIGHT or event.key==pygame.K_d )and dir != 'L':
                dir='R'


def snakegrewup():# 长在头上，不要pop
    head=snakesarry[0]
    if dir == 'L':
        snakesarry.insert(0, head.copy_toL())

    elif dir == 'R':
        snakesarry.insert(0, head.copy_toR())

    elif dir == 'U':
        snakesarry.insert(0, head.copy_toU())

    elif dir == 'D':
        snakesarry.insert(0, head.copy_toD())







def newfood():
        food=Point(row=random.randint(0,ROW-1), col=random.randint(0,COL-1))
        return food


def collision_test():
    head=snakesarry[0]
    if  (head.col<0 or head.col>COL ) or (head.row<0 or head.row >ROW):
        return 1
    for p in snakesarry[1:]:
        if head.row==p.row and head.col ==p.col:
            return 1
    return  0


def prompt(wintitle, text):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(wintitle, text)
    try:
        root.destroy()
    except:
        pass


window = pygame.display.set_mode(windowsize)
pygame.display.set_caption('snake')
playing = True
clock = pygame.time.Clock()

#------------------------------------------------------------------------------

while playing:
    head=snakesarry[0]
    pygame.draw.rect(window, bgcolor, (0, 0, W, H))
    eat=(food.col==head.col and food.row==head.row)
    if eat:
        snakegrewup()
        food = newfood()  # 是否产生食物
    event_listen()  # 控制方向
    snamke_move()   # 根据当前方向移动蛇


    # # 改变蛇头的方向
    if collision_test()==True:
        prompt('err','you die')

    paint_snake()
    rect(food,foodcolor)
    # 渲染，画出来
    pygame.display.flip()  # 控制交还给sys

    # 设置帧率
    clock.tick(16)

print('game over')
# 收尾工作

