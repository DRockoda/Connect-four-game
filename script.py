import numpy as np
import pygame
import sys
import math
from pygame import mixer

ROW_COUNT=6
COLUMN_COUNT=7

def create_board():
    board=np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board,row,col,piece):
    board[row][col]=piece

def is_valid_location(board,col):
    return board[ROW_COUNT-1][col]==0

def get_next_open_row(board,col):
    for r in range(ROW_COUNT):
        if board[r][col]==0:
            return r

def print_board(board):    
    print(np.flip(board,0))

def get_winning_move(board,piece):
    
    #horizontal check
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c]==piece and board[r][c+1]==piece and board[r][c+2]==piece and board[r][c+3]==piece:
                return True
    #vertical check
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c]==piece and board[r+1][c]==piece and board[r+2][c]==piece and board[r+3][c]==piece:
                return True

    #positive diagonal
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c]==piece and board[r+1][c+1]==piece and board[r+2][c+2]==piece and board[r+3][c+3]==piece:
                return True

    #negative diagonal
    for c in range(COLUMN_COUNT-3):
        for r in range(3,ROW_COUNT):
            if board[r][c]==piece and board[r-1][c+1]==piece and board[r-2][c+2]==piece and board[r-3][c+3]==piece:
                return True

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(win,(0,0,255),(c*square_size,r*square_size+square_size,square_size,square_size))
            pygame.draw.circle(win,(0,0,0),(int(c*square_size+square_size/2),int(r*square_size+square_size+square_size/2)),radius)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c]==1:
                pygame.draw.circle(win,(255,0,0),(int(c*square_size+square_size/2),height-int(r*square_size+square_size/2)),radius)
            elif board[r][c]==2:
                pygame.draw.circle(win,(255,255,0),(int(c*square_size+square_size/2),height-int(r*square_size+square_size/2)),radius)
    pygame.display.update()

board=create_board()
print_board(board)
game_over=False
turn =0

pygame.init()
square_size=100

pygame.display.set_caption("Connect 4")
icon=pygame.image.load("pool.png")
pygame.display.set_icon(icon)

width=COLUMN_COUNT*square_size
height=(ROW_COUNT+1)*square_size
size=(width,height)
radius=int(square_size/2-5)
win=pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
myfont=pygame.font.SysFont("monosapce",75)

while not game_over:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()

        if event.type==pygame.MOUSEMOTION:
            pygame.draw.rect(win,(0,0,0),(0,0,width,square_size))
            posx=event.pos[0]
            if turn == 0:
                pygame.draw.circle(win,(255,0,0),(posx,int(square_size/2)),radius)
            else:
                pygame.draw.circle(win,(255,255,0),(posx,int(square_size/2)),radius)
        pygame.display.update()

        if event.type==pygame.MOUSEBUTTONDOWN:
            coin_sound=mixer.Sound("coin.wav")
            coin_sound.play()
            pygame.draw.rect(win,(0,0,0),(0,0,width,square_size))
            if turn ==0:
                posx=event.pos[0]
                col=int(math.floor(posx/square_size))

                if is_valid_location(board,col):
                    row=get_next_open_row(board,col)
                    drop_piece(board,row,col,1)

                    if get_winning_move(board,1):
                        print("Player 1 wins!!!")
                        label=myfont.render("Player 1 wins!!",1,(255,0,0))
                        win.blit(label,(40,10))
                        game_over=True
                        

            else:
                posx=event.pos[0]
                col=int(math.floor(posx/square_size))

                if is_valid_location(board,col):
                    row=get_next_open_row(board,col)
                    drop_piece(board,row,col,2)

                    if get_winning_move(board,2):
                        print("Player 2 wins!!!")
                        label=myfont.render("Player 2 wins!!",1,(255,255,0))
                        win.blit(label,(40,10))
                        game_over=True
                        

            print_board(board)
            draw_board(board)
            turn += 1
            turn =turn %2

            if game_over:
                pygame.time.wait(5000)