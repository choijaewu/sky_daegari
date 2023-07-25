class playerAction:
    def __init__(self):
        self.max_health = 5
        self.current_health = self.max_health
        self.max_cost = 3
        self.current_cost = self.max_cost
        self.critical = 25
        self.defending = 0

    def damaged(self, damage):
        real_damage = damage - self.defending
        self.current_health -= real_damage
        if self.current_health > 0:
            return self.current_health
        else:
            return -1

    def usecost(self, amount):
        if self.current_cost > amount:
            self.current_cost -= amount
            return self.current_cost
        else:
            return -1
    
    def health_recover(self, recovering):
        self.current_health += recovering
        return self.current_health
    
    def health_increase(self, increasing):
        self.max_health += increasing
        self.current_health += increasing
        return self.current_health

    def cost_recover(self, recovering):
        self.current_cost += recovering
        return self.current_cost
    
    def cost_increase(self, increasing):
        self.max_cost += increasing
        self.current_cost += increasing
        return self.current_cost
    
class enemy_1Action:
    def __init__(self, enemy_type):
        if enemy_type == 1:
            self.health = 3
            self.deal = 1
            self.defending = 0
        elif enemy_type == 2:
            self.health = 5
            self.deal = 2
            self.defending = 0
        elif enemy_type == 3:
            self.health = 8
            self.deal = 3
            self.defending = 0
        elif enemy_type == 4:
            self.health = 15
            self.deal = 4
            self.defending = 3

        self.typenum = enemy_type

    def damaged(self, damage):
        real_damage = damage - self.defending
        self.health -= real_damage
        if self.health > 0:
            return self.health
        else:
            return -1

    

import pygame
import random


pygame.init() #초기화


background_image = pygame.image.load("")

player_image = pygame.image.load("")

enemy_1_image = pygame.image.load("")
enemy_2_image = pygame.image.load("")
enemy_3_image = pygame.image.load("")
boss_image = pygame.image.load("")

chest_image = pygame.image.load("")


player = playerAction() #class 생성


enemy_xlocation = [i for i in range(600, 950, 50)] #적 x좌표

playerturn = 1 #플레이어 턴인가?

screan = pygame.display.set_mode((1200,700)) #게임 창 크기
pygame.display.set_caption("게임이름") #게임 창 이름


running = 1 #게임이 실행중인가?


while running:
    for event in pygame.event.get(): #이벤트 입력
        if event.type == pygame.QUIT: #X버튼 눌렀을 때
            running = 0 #프로그램 종료
        
    
    screan.blit(background_image, (0,0))
    screan.blit(player_image,(300, 350))

    pygame.display.update()


pygame.quit() #종료 