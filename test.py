import pygame
import random
import time
from pyc import *
from pygame.sprite import AbstractGroup

pygame.init() #초기화

name = '' #플레이어 이름

running = 1

message_time = 0 #메세지 띄우는 시간
koreanfont = pygame.font.SysFont('malgungothic',30) #한글 폰트(맑은고딕)

background_image = pygame.image.load("background.png") #배경이미지
chest_image = pygame.image.load("상자.png") #상자이미지
chestweapon = pygame.image.load("상자무기.png")
chestshield = pygame.image.load("상자방패.png")
chestfood = pygame.image.load("상자음식.png")
background_image = pygame.transform.scale(background_image, (1300, 700))
chest_image = pygame.transform.scale(chest_image, (250, 250))
chestweapon = pygame.transform.scale(chestweapon, (200, 280))
chestshield = pygame.transform.scale(chestshield, (200, 280))
chestfood = pygame.transform.scale(chestfood, (200, 280))
cwinfo = [100, 100, 300, 380]
csinfo = [500, 100, 700, 380]
cfinfo = [900, 100, 1100, 380]

screen_width, screen_height = 1300, 700 #화면 넓이, 높이
screen = pygame.display.set_mode((screen_width, screen_height)) #게임 창 크기
pygame.display.set_caption("김건후") #게임 창 이름
clock = pygame.time.Clock()

enemy_xlocation = [600, 710, 820, 930, 1040, 1150] #적 x좌표
enemy_ylocation = [350, 340, 340, 300] #적 y좌표

cardlist = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #카드를 가지고 있는가?




images = ['초급몬스터.png','중급몬스터.png','상급몬스터.png','보스.png']
scales = [(100, 100), (100, 100), (100, 100), (150, 150)]
types = [1, 1, 1, 2 , 3, 4]
cardimages = ['단검.png','장검.png','독화살.png','불화살.png','얼음화살.png','낡은방패.png','방패.png','최후의방패.png','음료수.png','물약.png', '고기.png']


while running:
        for event in pygame.event.get(): #이벤트 입력
            if event.type == pygame.QUIT: #X버튼 눌렀을 때
                running = 0 #프로그램 종료
        screen.blit(background_image, (0,0))
        for i in range(6):
            enemy_type = types[i]
            enemy_image = pygame.image.load(images[enemy_type - 1])
            enemy_image = pygame.transform.scale(enemy_image, scales[enemy_type - 1])
            rect = enemy_image.get_rect()
            
            screen.blit(enemy_image, (enemy_xlocation[i], enemy_ylocation[enemy_type - 1]))

        cnt = 0
        for i in range(25, 1300, 160):
             cardimage = pygame.image.load(cardimages[cnt])
             cardimage = pygame.transform.scale(cardimage, (130, 190))
             screen.blit(cardimage, (i, 480))
             cnt+=1
        for i in range(425, 876, 160):
             cardimage = pygame.image.load(cardimages[cnt])
             cardimage = pygame.transform.scale(cardimage, (130, 190))
             screen.blit(cardimage, (i, 30))
             cnt+=1
        pygame.display.flip()

pygame.quit