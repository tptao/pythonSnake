import pygame
import random
import tkinter as tk
from tkinter import messagebox
pygame.init()
pygame.display.set_caption('snake')
clock = pygame.time.Clock()


bgcolor   = (255, 255, 0)
headcolor = (255, 0, 0)
bodycolor = (100, 20, 125)
foodcolor = (255, 0, 200)
tailcolor = (0, 0, 0)

class Random_pos():
    def __init__(self,gmap):
        self.row=random.randint(0,gmap.ROW-1)
        self.col=random.randint(0,gmap.COL-1)


class Node():
    def __init__(self,row,col,dir):
        self.row=row
        self.col=col
        self.dir=dir

    def copy(self):
        if self.dir=='L':
            return Node(row=self.row, col=self.col-1,dir=self.dir)
        if self.dir=='R':
            return Node(row=self.row, col=self.col + 1,dir=self.dir)
        if self.dir=='U':
            return Node(row=self.row-1, col=self.col,dir=self.dir)
        if self.dir=='D':
            return Node(row=self.row+1, col=self.col,dir=self.dir)

    def new(self, gmap):
        foodnode = Node(random.randint(0, gmap.ROW - 1), random.randint(0, gmap.COL - 1),self.dir)
        return foodnode

    def draw_rectangle(self, color,gmap,window):
        left = self.col * gmap.cellwidth
        top = self.row * gmap.cellheight
        pos_info = (left, top, gmap.cellwidth, gmap.cellheight)

        pygame.draw.rect(window, color, pos_info)

    def draw(self, color,gmap,window):
        self.draw_rectangle(color,gmap,window)


class Gmap():
    def __init__(self,width,height,col,row):
        self.WIDTH=width
        self.HEIGHT=height
        self.ROW=row
        self.COL=col
        self.cellwidth = self.WIDTH / self.COL
        self.cellheight = self.HEIGHT / self.ROW

    def drawMap(self):
        mapsize=(self.WIDTH, self.HEIGHT)
        window = pygame.display.set_mode(mapsize)
        pygame.draw.rect(window, (255, 255, 0), (0, 0, self.WIDTH, self.HEIGHT))
        return  window



class Snake():
    def __init__(self,gmap):
        node = Node(random.randint(0, gmap.ROW - 1), random.randint(0, gmap.COL - 1),'L')
        self.body = [node]

    
    def growup(self):
        head = self.body[0]
        self.body.insert(0, head.copy())

    def move(self):
        head = self.body[0] # head在不断的动态刷新
        # 沿着蛇头移动
        self.body.insert(0, head.copy())
        self.body.pop()
        print('go')

    def collision(self,gmap):
        head = self.body[0]
        if (head.col < 0 or head.col > gmap.COL) or (head.row < 0 or head.row > gmap.ROW):
            return 1
        for p in self.body[1:]:
            if head.row == p.row and head.col == p.col:
                return 1
        return 0

    def draw_rectangle(self,node, color,gmap,window):
        left = node.col * gmap.cellwidth
        top  = node.row * gmap.cellheight
        pos_info=(left, top, gmap.cellwidth, gmap.cellheight)

        pygame.draw.rect(window, color, pos_info )

    def draw_snake(self,color,gmap,window):
        head = self.body[0]
        for point in self.body:
            self.draw_rectangle(point, color,gmap, window)
        self.draw_rectangle(head, color,gmap, window)
                





class Game():
    def __init__(self):
        self.playing=True

    def event_listen(self,snake):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                pygame.quit()  # shout down window

            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and dir != 'U':
                    snake.body[0].dir = 'D'
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and dir != 'D':
                    snake.body[0].dir = 'U'
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and dir != 'R':
                    snake.body[0].dir = 'L'
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and dir != 'L':
                    snake.body[0].dir = 'R'

#-----------------------------创建对象

gameMap=Gmap(800,600,80,60)
random_pos=Random_pos(gameMap)
food=Node(random_pos.row,random_pos.col,'R')
snake=Snake(gameMap)


game=Game()


while game.playing==True:

    window = gameMap.drawMap()

    head = snake.body[0]



    eat = (food.col == head.col and food.row == head.row)
    if eat:
        snake.growup()
        food = food.new(gameMap)
    game.event_listen(snake)
    snake.move()  # 根据当前方向移动蛇

    food.draw(foodcolor,gameMap,window)

    # # 改变蛇头的方向
    if snake.collision(gameMap)== True:
        pass

    snake.draw_snake(bodycolor,gameMap,window)
    # 渲染，画出来
    pygame.display.flip()  # 控制交还给sys

    # 设置帧率
    clock.tick(16)