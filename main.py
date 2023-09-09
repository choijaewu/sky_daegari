from typing import Any
import pygame
import random
import time
from pyc import *
from pygame.sprite import AbstractGroup

pygame.init() #초기화

name = '' #플레이어 이름

background_image = pygame.image.load("images/background.png") #배경이미지
healthimage = pygame.image.load('images/체력.png')
costimage = pygame.image.load('images/코스트.png')
poisonedimage = pygame.image.load('images/중독.png')
stunnedimage = pygame.image.load('images/스턴.png')
dealimage = pygame.image.load('images/공격.png')
defendingimage = pygame.image.load('방어.png')
cardimages = ['images/단검.png','images/장검.png','images/독화살.png','images/불화살.png','images/얼음화살.png','images/낡은방패.png',
                'images/방패.png','images/최후의방패.png','images/음료수.png','images/물약.png', 'images/고기.png']
background_image = pygame.transform.scale(background_image, (1300, 700))
healthimage = pygame.transform.scale(healthimage, (75, 75))
costimage = pygame.transform.scale(costimage, (60, 60))
poisonedimage = pygame.transform.scale(poisonedimage, (50,50))
stunnedimage = pygame.transform.scale(stunnedimage, (50,50))
dealimage = pygame.transform.scale(dealimage, (30, 30))
defendingimage = pygame.transform.scale(defendingimage, (50,50))

screen_width, screen_height = 1300, 700 #화면 넓이, 높이
screen = pygame.display.set_mode((screen_width, screen_height)) #게임 창 크기
pygame.display.set_caption("새벽의 용사") #게임 창 이름
clock = pygame.time.Clock()

koreanfont = pygame.font.SysFont('malgungothic',30) #한글 폰트(맑은고딕)
message_time = 0 #메세지 띄우는 시간
message = koreanfont.render('',True, (255, 255, 255))
message_rect = message.get_rect()
message_rect.center = (screen_width//2, 40)

enemy_xlocation = [600, 710, 820, 930, 1040, 1150] #적 x좌표
enemy_ylocation = [350, 340, 340, 300] #적 y좌표

cardlist = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0] #카드를 가지고 있는가?

running = True #게임이 실행중인가?
gaming = True #스테이지 진행중인가?

class playerSprite(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.player_image = pygame.image.load(image)
        self.player_image = pygame.transform.scale(self.player_image, (128, 128))
        self.rect = self.player_image.get_rect()
        self.rect.topleft = position
        self.player_position = self.rect.center = position
        self.max_health = self.current_health = 5
        self.max_cost = self.current_cost = 3
        self.critical = 25
        self.defending = 0

    def damaged(self, damage):
        real_damage = 0
        if damage >= self.defending: 
            real_damage = damage - self.defending
            self.defending = 0
        else: self.defending -= damage
        self.current_health -= real_damage
        if self.current_health < 0: self.current_health = 0

    def increase_defense(self, amount):
        self.defending += amount

    def canUse(self, cost):
        return self.current_cost >= cost

    def usecost(self, amount):
        self.current_cost -= amount

    
    def health_increase(self, increasing):
        self.max_health += increasing
        self.current_health += increasing

    def cost_recover(self, recovering):
        self.current_cost += recovering
        if self.current_cost > self.max_cost: self.current_cost = self.max_cost
    
    def cost_increase(self, increasing):
        self.max_cost += increasing
        self.current_cost += increasing
    
class enemySprite(pygame.sprite.Sprite):
    def __init__(self, enemy_type, position):
        pygame.sprite.Sprite.__init__(self)
        images = ['images/초급몬스터.png','images/중급몬스터.png','images/상급몬스터.png','images/보스.png']
        scales = [(100, 100), (100, 100), (100, 100), (150, 150)]
        self.enemy_image = pygame.image.load(images[enemy_type - 1])
        self.enemy_image = pygame.transform.scale(self.enemy_image, scales[enemy_type - 1])
        self.enemy_position = position
        self.rect = self.enemy_image.get_rect()
        self.rect.topleft = position

        info = [[3,1,0], [5,2,0], [8,3,0], [15,4,1]]
        self.health = info[enemy_type - 1][0]
        self.deal = info[enemy_type - 1][1]
        self.defending = info[enemy_type - 1][2]
        self.enemy_type = enemy_type
        self.condition = 'none'
        if enemy_type == 4:
            self.skill_turn = 3 #스킬 쿨타임
        
    def damaged(self, damage):
        real_damage = damage - self.defending
        self.health -= real_damage
        if self.health <= 0: self.health = 0
    
    def boss_skill(self, enemies):
        enemy = enemySprite(randomEnemy(5,3,2), (enemy_xlocation[len(enemies)], enemy_ylocation))
        if len(enemies) < 6: enemies.insert(enemies.index(self), enemy)
        self.skill_turn = 3

class cardSprite(pygame.sprite.Sprite):
    def __init__(self, card_type):
        pygame.sprite.Sprite.__init__(self)
        global cardimages

        costs = [1, 1, 1, 1, 1, 1, 2, 3, 1, 1, 1] #단검 장검 독화살 불화살 얼음화살 낡은방패 방패 최후의방패 음료수 물약 고기
        positions = [(25, 480), (185, 480), (345, 480), (505, 480), (665, 480), (825, 480), (985, 480), (1145, 480),
                     (425, 70), (585, 70), (745, 70)]
        self.card_image = pygame.image.load(cardimages[card_type - 1])
        self.card_image = pygame.transform.scale(self.card_image, (130, 190))
        self.card_cost = costs[card_type - 1]
        self.card_position = positions[card_type - 1]
        self.rect = self.card_image.get_rect()
        self.rect.topleft = self.card_position
        self.card_type = card_type
    
    def useCard(self, enemies, player, cards):
        global running
        global gaming
        global message_time
        global message
        global message_rect


        if player.canUse(self.card_cost):
            chosen = 0
            if self.card_type  == 1 or self.card_type == 2 or self.card_type== 3 or self.card_type== 4 or self.card_type== 5:
                enemychoosing = True
                while enemychoosing:
                    message = koreanfont.render("공격할 적을 선택해주세요.", True, (255,255,255))
                    message_rect = message.get_rect()
                    message_rect.center = (screen_width//2, 40)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            gaming = False
                            enemychoosing = False
                            break

                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                mouseposition = pygame.mouse.get_pos()
                                for enemy in enemies:
                                    if enemy.rect.collidepoint(mouseposition):
                                        chosen = enemies.index(enemy)
                                        enemychoosing = False
                                        break
                    screenupdate(screen, player, enemies, cards)
                enemy = enemies[chosen]

            player.usecost(self.card_cost)
            if self.card_type == 1:       #단검
                enemy.damaged(1)

            elif self.card_type == 2:     #장검
                enemy.damaged(1)
                if chosen+1 < len(enemies):
                    enemy2 = enemies[chosen+1]
                    enemy2.damaged(1)

            elif self.card_type == 3:     #독화살
                enemy.damaged(2)
                enemy.condition = 'poisoned'

            elif self.card_type == 4:     #불화살
                enemy.damaged(3)

            elif self.card_type == 5:     #얼음화살
                enemy.damaged(2)
                enemy.condition = 'stunned'
            
            elif self.card_type == 6:     #낡은 방패
                player.increase_defense(1)

            elif self.card_type == 7:    #방패
                player.increase_defense(3)

            elif self.card_type == 8:   #최후의 방패
                player.increase_defense(5)

            elif self.card_type == 9:   #음료수
                player.cost_increase(1)
                cards.remove(self)
                cardlist[8] = 0

            elif self.card_type == 10:   #물약
                player.cost_recover(4)
                cards.remove(self)
                cardlist[9] = 0

            elif self.card_type == 11:   #고기
                player.health_increase(2)
                cards.remove(self)
                cardlist[10] = 0

                
        else: 
            message = koreanfont.render('코스트가 부족합니다',True, (255, 255, 255))
            message_rect = message.get_rect()
            message_rect.center = (screen_width//2, 40)
            message_time = 1 #game loop에서 초 줄이며 메시지 띄우기

def randomEnemy(first, second, third):
    li = []
    for _ in range(first): li.append(1)
    for _ in range(second): li.append(2)
    for _ in range(third): li.append(3)
    choiced = random.choice(li)
    return choiced

def makeStage(stage):
    global enemy_xlocation
    global enemy_ylocation
    enemies = []
    if stage == 1:
        for i in range(3):
            enemy = enemySprite(1, (enemy_xlocation[i], enemy_ylocation[0]))
            enemies.append(enemy)
    elif stage == 2:
        for i in range(4):
            enemy_type = randomEnemy(9,1,0)
            enemy = enemySprite(enemy_type, (enemy_xlocation[i], enemy_ylocation[enemy_type - 1]))
            enemies.append(enemy)
    elif stage == 3:
        for i in range(4):
            enemy_type = randomEnemy(7,2,1)
            enemy = enemySprite(enemy_type, (enemy_xlocation[i], enemy_ylocation[enemy_type - 1]))
            enemies.append(enemy)
    elif stage == 4:
        for i in range(3):
            enemy_type = randomEnemy(6,3,1)
            enemy = enemySprite(enemy_type, (enemy_xlocation[i], enemy_ylocation[enemy_type - 1]))
            enemies.append(enemy)
    elif stage == 5:
        for i in range(4):
            enemy_type = randomEnemy(5,3,2)
            enemy = enemySprite(enemy_type, (enemy_xlocation[i], enemy_ylocation[enemy_type - 1]))
            enemies.append(enemy)
    elif stage == 6:
        for i in range(5):
            enemy_type = randomEnemy(5,3,2)
            enemy = enemySprite(enemy_type, (enemy_xlocation[i], enemy_ylocation[enemy_type - 1]))
            enemies.append(enemy)
    elif stage == 7:
        enemy_type = randomEnemy(5,3,2)
        enemy = enemySprite(enemy_type, (enemy_xlocation[0], enemy_ylocation[enemy_type - 1]))
        enemies.append(enemy)
        enemy = enemySprite(4, (enemy_xlocation[1], enemy_ylocation[3]))
        enemies.append(enemy)
    return enemies

def start_story():
    global running

    #색 정의
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    purple = (148, 0, 211)

    start_time = pygame.time.get_ticks()

    #text정의
    text_info = [
        #["이곳은 새벽의 나라", white],
        #["다른 나라에 비해 발전은 늦지만", white],
        #["높은 인망으로 호평을 받는 곳이다.", white],
        #["그런데", red],
        #["땅이 갈라지며 나타난", white],
        #["절망의 군대", purple],
        #["그들은 모든 건물을 불태우고 사람들을 죽였다.", white],
        #["그러나 나라를 구하기 위해 나타난 전사", white],
        #["그는 곧장 절망의 미로로 들어갔고", white],
        #["적을 섬멸해 나간다.", white],
        ["그의 이름은 바로...", white]
        ]

    current_text = text_info[0][0]
    text_color = text_info[0][1]
    text = koreanfont.render(current_text, True, text_color)
    text_rect = text.get_rect()
    text_rect.center = (screen_width // 2, screen_height // 2)#화면 중앙


    screen.fill(black)

    i = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(text,text_rect)

        current_time = pygame.time.get_ticks()
        if current_time - start_time >= len(text_info[i][0])*100 + 800:  #여기서 시간을 계산
            i += 1
            if len(text_info) > i:
                current_text = text_info[i][0]
                text_color = text_info[i][1]

                screen.fill(black)
                text = koreanfont.render(current_text, True, text_color)
                text_rect = text.get_rect()
                text_rect.center = (screen_width // 2, screen_height // 2)

                start_time = pygame.time.get_ticks()

            else:
                nameinput()
                game_loop()
                
        pygame.display.flip()

    pygame.quit()

def nameinput():
    global running
    global name

    name = ''
    inputing = True
    text = koreanfont.render("이름을 입력해주세요", True, (255, 255, 255))
    while inputing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                inputing = False
                break
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    time.sleep(0.3)
                    inputing = False
                    break
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1] #맨 오른쪽 값 제외하고 대입
                else:
                    name += event.unicode #입력한 문자 추가
                text = koreanfont.render(name, True, (255, 255, 255))
        
        screen.fill((0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (screen_width // 2, screen_height // 2)
        screen.blit(text, text_rect)
        pygame.display.flip()

def game_loop():
    global message_time
    global message
    global message_rect
    global running
    global gaming

    player = playerSprite("images/player.png", (300, 320)) #class 생성

    running = 1 #게임이 실행중인가?
    playerturn = 1 #플레이어 턴인가?
    stage = 1 #스테이지
    enemies = makeStage(stage)
    cards = pygame.sprite.Group()
    cards.add(cardSprite(1)) #단검
    cards.add(cardSprite(6)) #낡은방패

    while gaming:
        for event in pygame.event.get(): #이벤트 입력
            if event.type == pygame.QUIT: #X버튼 눌렀을 때
                gaming = False
                running = False #게임 종료
        
        if playerturn:
            message = koreanfont.render('당신의 차례입니다.',True, (255, 255, 255))
            message_rect = message.get_rect()
            message_rect.center = (screen_width//2, 40)
            if pygame.mouse.get_pressed()[0]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for card in cards:
                    if card.rect.collidepoint(mouse_x, mouse_y):
                        card.useCard(enemies, player, cards)
                        if player.current_cost == 0:
                            playerturn = 0

                        i = 0
                        while i < len(enemies):
                            enemy = enemies[i]
                            if enemy.health <= 0: 
                                enemies.remove(enemy)
                                i-=1
                            i+=1

                        if len(enemies) == 0:
                            screenupdate(screen, player, enemies, cards)
                            time.sleep(0.5) #잠시대기
                            if stage == 7:
                                ending_story() #마지막 스테이지면 엔딩
                                running = False
                                gaming = False
                                break
                            else:
                                chest(cards) #아니면 상자
                                stage += 1
                                enemies = makeStage(stage)
                                playerturn = 1
                                player.current_health = player.max_health
                                player.current_cost = player.max_cost

        else:
            message = koreanfont.render('적의 차례입니다.',True, (255, 255, 255))
            message_rect = message.get_rect()
            message_rect.center = (screen_width//2, 40)
            screenupdate(screen, player, enemies, cards)
            time.sleep(0.5)
            for enemy in enemies:
                if enemy.condition == 'stunned':
                    enemy.condition = 'none'
                    time.sleep(0.5)
                    if enemy.enemy_type == 4:
                        if enemy.skill_turn == 0: enemy.boss_skill(enemies)
                        else: enemy.skill_turn -= 1
                else:
                    player.damaged(enemy.deal)
                    screenupdate(screen, player, enemies, cards)
                    time.sleep(0.5)
                    if player.current_health <= 0:
                        screenupdate(screen, player, enemies, cards)
                        time.sleep(0.5)
                        death_story()
                        gaming = False
                        running = False
                        break
                if enemy.condition == 'poisoned':
                    enemy.condition = 'none'
                    enemy.damaged(2)
                    while i < len(enemies):
                        enemy = enemies[i]
                        if enemy.health <= 0: 
                            enemies.remove(enemy)
                            i-=1
                        i+=1
                screenupdate(screen, player, enemies, cards)
            playerturn = 1
            player.current_cost = player.max_cost

        screenupdate(screen, player, enemies, cards)

def screenupdate(screen, player, enemies, cards):
    global background_image
    global message_time
    global message
    global message_rect
    global healthimage
    global costimage
    global stunnedimage
    global poisonedimage
    global dealimage
    global defendingimage

    screen.blit(background_image, (0,0)) #배경이미지
    screen.blit(player.player_image, player.player_position)

    healthmessage = koreanfont.render(str(player.current_health), True, (0, 0, 0))
    costmessage = koreanfont.render(str(player.current_cost), True, (0, 0, 0))
    defendingmessage = koreanfont.render(str(player.defending), True, (0, 0, 0))
    healthimage_rect = healthimage.get_rect()
    costimage_rect = costimage.get_rect()
    defendingimage_rect = defendingimage.get_rect()
    healthmessage_rect = healthmessage.get_rect()
    costmessage_rect = costmessage.get_rect()
    defendingmessage_rect = defendingmessage.get_rect()
    healthmessage_rect.center = healthimage_rect.center = (player.player_position[0]+30,  player.player_position[1]-30)
    costmessage_rect.center = costimage_rect.center = (player.player_position[0]+80,  player.player_position[1]-27)
    defendingmessage_rect.center = defendingimage_rect.center = (player.player_position[0]+120,  player.player_position[1]-27)

    screen.blit(healthimage, healthimage_rect)
    screen.blit(healthmessage, healthmessage_rect)
    screen.blit(costimage, costimage_rect)
    screen.blit(costmessage, costmessage_rect)
    screen.blit(defendingimage, defendingimage_rect)
    screen.blit(defendingmessage, defendingmessage_rect)

    if message_time > 0:
        message = koreanfont.render('코스트가 부족합니다',True, (255, 255, 255))
        message_rect = message.get_rect()
        message_rect.center = (screen_width//2, 40)
        message_time -= 0.2
    screen.blit(message, message_rect)

    for enemy in enemies:
        dealimage_rect = dealimage.get_rect()
        dealimage_rect.center = (enemy.enemy_position[0] - 20, enemy.enemy_position[1]+15)
        dealmessage = koreanfont.render(str(enemy.deal), True, (255, 0, 0))
        dealmessage_rect = dealmessage.get_rect()
        dealmessage_rect.center = (enemy.enemy_position[0], enemy.enemy_position[1]+12)
        healthmessage = koreanfont.render(str(enemy.health), True, (0, 0, 0))
        healthmessage_rect = healthmessage.get_rect()
        defendingmessage = koreanfont.render(str(enemy.defending), True, (0, 0, 0))
        defendingmessage_rect = defendingmessage.get_rect()
        healthmessage_rect.center = healthimage_rect.center = (enemy.enemy_position[0]+30,  enemy.enemy_position[1]-30)
        defendingmessage_rect.center = defendingimage_rect.center = (enemy.enemy_position[0]+70,  enemy.enemy_position[1]-30)
        screen.blit(enemy.enemy_image, enemy.enemy_position)
        screen.blit(healthimage, healthimage_rect)
        screen.blit(healthmessage, healthmessage_rect)
        screen.blit(dealimage, dealimage_rect)
        screen.blit(dealmessage, dealmessage_rect)
        screen.blit(defendingimage, defendingimage_rect)
        screen.blit(defendingmessage, defendingmessage_rect)
        if enemy.condition == 'stunned':
            stunnedimage_rect = stunnedimage.get_rect()
            stunnedimage_rect.center = (enemy.enemy_position[0] - 5, enemy.enemy_position[1]+45)
            screen.blit(stunnedimage, stunnedimage_rect)
        if enemy.condition == 'poisoned':
            poisonedimage_rect = poisonedimage.get_rect()
            poisonedimage_rect.center = (enemy.enemy_position[0] - 5, enemy.enemy_position[1]+75)
            screen.blit(poisonedimage, poisonedimage_rect)
    for card in cards: screen.blit(card.card_image, card.card_position)


    pygame.display.flip()
    clock.tick(10) #FPS

def chest(cards):
    global cardlist
    global running
    global background_image
    global cardimages
    global message
    global message_rect

    cardcnt = sum(cardlist)

    if cardcnt < 10: message = koreanfont.render("카드 2개를 선택해주세요", True, (255,255,255))
    else: message = koreanfont.render("카드 1개를 선택해주세요", True, (255,255,255))
    
    chest_image = pygame.image.load("images/상자.png") #상자이미지
    chestweapon = pygame.image.load("images/상자무기.png")
    chestshield = pygame.image.load("images/상자방패.png")
    chestfood = pygame.image.load("images/상자음식.png")
    chest_image = pygame.transform.scale(chest_image, (250, 250))
    chestweapon = pygame.transform.scale(chestweapon, (200, 280))
    chestshield = pygame.transform.scale(chestshield, (200, 280))
    chestfood = pygame.transform.scale(chestfood, (200, 280))
    cwinfo = [150, 150, 350, 430]
    csinfo = [550, 150, 750, 430]
    cfinfo = [950, 150, 1150, 430]

    choosing = True
    weaponlist = []
    shieldlist = []
    foodlist = []
    for w in range(5):
        if not cardlist[w]: weaponlist.append(w+1)
    for s in range(5, 8):
        if not cardlist[s]: shieldlist.append(s+1)
    for f in range(8, 11):
        if not cardlist[f]: foodlist.append(f+1)
    weapon = shield = food = 0
    if len(weaponlist) != 0: weapon = random.choice(weaponlist)
    if len(shieldlist) != 0: shield = random.choice(shieldlist)
    if len(foodlist) != 0: food = random.choice(foodlist)
    print(weaponlist, shieldlist, foodlist)
    print(weapon, shield, food)
    print(cardcnt)
    
    cnt = 0
    while choosing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                choosing = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                if cwinfo[0] < mx and mx < cwinfo[2] and cwinfo[1] < my and my < cwinfo[3] and weapon:
                    cards.add(cardSprite(weapon))
                    cardlist[weapon - 1] = 1
                    if cnt < 1:
                        firstcard = pygame.image.load(cardimages[weapon - 1])
                        firstcard = pygame.transform.scale(firstcard, (200, 280))
                        firstcardposition = (150, 150)
                    if cardcnt > 9:
                        screen.blit(background_image, (0,0))
                        screen.blit(chest_image, (525, 450))
                        screen.blit(message, message_rect)
                        if weapon: screen.blit(chestweapon, cwinfo[:2])
                        if shield: screen.blit(chestshield, csinfo[:2])
                        if food: screen.blit(chestfood, cfinfo[:2])
                        screen.blit(firstcard, firstcardposition)
                        pygame.display.flip()
                        choosing = False
                        time.sleep(0.7)
                    elif cnt == 1:
                        secondcard = pygame.image.load(cardimages[weapon - 1])
                        secondcard = pygame.transform.scale(secondcard, (200, 280))
                        secondcardposition = (150, 150)
                        screen.blit(background_image, (0,0))
                        screen.blit(chest_image, (525, 450))
                        screen.blit(message, message_rect)
                        if weapon: screen.blit(chestweapon, cwinfo[:2])
                        if shield: screen.blit(chestshield, csinfo[:2])
                        if food: screen.blit(chestfood, cfinfo[:2])
                        screen.blit(firstcard, firstcardposition)
                        screen.blit(secondcard, secondcardposition)
                        pygame.display.flip()
                        choosing = False
                        time.sleep(0.7)
                    cnt += 1
                elif csinfo[0] < mx and mx < csinfo[2] and csinfo[1] < my and my < csinfo[3] and shield:
                    cards.add(cardSprite(shield))
                    cardlist[shield - 1] = 1
                    if cnt < 1:
                        firstcard = pygame.image.load(cardimages[shield - 1])
                        firstcard = pygame.transform.scale(firstcard, (200, 280))
                        firstcardposition = (550, 150)
                    if cardcnt > 9:
                        screen.blit(background_image, (0,0))
                        screen.blit(chest_image, (525, 450))
                        screen.blit(message, message_rect)
                        if weapon: screen.blit(chestweapon, cwinfo[:2])
                        if shield: screen.blit(chestshield, csinfo[:2])
                        if food: screen.blit(chestfood, cfinfo[:2])
                        screen.blit(firstcard, firstcardposition)
                        pygame.display.flip()
                        choosing = False
                        time.sleep(0.7)
                    elif cnt == 1:
                        secondcard = pygame.image.load(cardimages[shield - 1])
                        secondcard = pygame.transform.scale(secondcard, (200, 280))
                        secondcardposition = (550, 150)
                        screen.blit(background_image, (0,0))
                        screen.blit(chest_image, (525, 450))
                        screen.blit(message, message_rect)
                        if weapon: screen.blit(chestweapon, cwinfo[:2])
                        if shield: screen.blit(chestshield, csinfo[:2])
                        if food: screen.blit(chestfood, cfinfo[:2])
                        screen.blit(firstcard, firstcardposition)
                        screen.blit(secondcard, secondcardposition)
                        pygame.display.flip()
                        choosing = False
                        time.sleep(0.7)
                    cnt += 1
                elif cfinfo[0] < mx and mx < cfinfo[2] and cfinfo[1] < my and my < cfinfo[3] and food:
                    cards.add(cardSprite(food))
                    cardlist[food - 1] = 1
                    if cnt < 1:
                        firstcard = pygame.image.load(cardimages[food - 1])
                        firstcard = pygame.transform.scale(firstcard, (200, 280))
                        firstcardposition = (950, 150)
                    if cardcnt > 9:
                        screen.blit(background_image, (0,0))
                        screen.blit(chest_image, (525, 450))
                        screen.blit(message, message_rect)
                        if weapon: screen.blit(chestweapon, cwinfo[:2])
                        if shield: screen.blit(chestshield, csinfo[:2])
                        if food: screen.blit(chestfood, cfinfo[:2])
                        screen.blit(firstcard, firstcardposition)
                        pygame.display.flip()
                        choosing = False
                        time.sleep(0.7)
                    elif cnt == 1:
                        secondcard = pygame.image.load(cardimages[food - 1])
                        secondcard = pygame.transform.scale(secondcard, (200, 280))
                        secondcardposition = (950, 150)
                        screen.blit(background_image, (0,0))
                        screen.blit(chest_image, (525, 450))
                        screen.blit(message, message_rect)
                        if weapon: screen.blit(chestweapon, cwinfo[:2])
                        if shield: screen.blit(chestshield, csinfo[:2])
                        if food: screen.blit(chestfood, cfinfo[:2])
                        screen.blit(firstcard, firstcardposition)
                        screen.blit(secondcard, secondcardposition)
                        pygame.display.flip()
                        choosing = False
                        time.sleep(0.7)
                    cnt += 1
        
        screen.blit(background_image, (0,0))
        screen.blit(chest_image, (525, 450))
        screen.blit(message, message_rect)
        if weapon: screen.blit(chestweapon, cwinfo[:2])
        if shield: screen.blit(chestshield, csinfo[:2])
        if food: screen.blit(chestfood, cfinfo[:2])
        if cnt >= 1: screen.blit(firstcard, firstcardposition)
        pygame.display.flip()

def ending_story():
    global name
    
    #색 정의
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    purple = (148, 0, 211)

    start_time = pygame.time.get_ticks()

    #text정의
    text_info = [
        ["영웅은 숨이 가빠옵니다.", white],
        ["그러나 헬의 상황은 더 나빠보이는군요.", white],
        ["헬이 말합니다.", white],
        ["나의 힘이 빠져나가는군", red],
        ["너를 흡수하고 완전체가 되었다면 나의 세상이 되었을 것을", red],
        ["하지만 잊지마라,", purple],
        ["나는 언젠가 다시 돌아올것이다.", white],
        ["그렇게 헬은 먼지가 되어 사라져 갑니다.", white],
        ["이제 그는 세상을 지킨 영웅이 되었군요.", white],
        ["그에게 찬사를 보내며 다시 한번 그의 이름을 말해봅니다.", white],
        [f"그의 이름은 바로 {name}입니다.", white],
        ]

    current_text = text_info[0][0]
    text_color = text_info[0][1]
    text = koreanfont.render(current_text, True, text_color)
    text_rect = text.get_rect()
    text_rect.center = (screen_width // 2, screen_height // 2)#화면 중앙


    screen.fill(black)

    storying = True
    i = 0
    while storying:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                storying = False

        screen.blit(text,text_rect)

        current_time = pygame.time.get_ticks()
        if current_time - start_time >= len(text_info[i][0])*100 + 800:  #여기서 시간을 계산
            i += 1
            if len(text_info) > i:
                current_text = text_info[i][0]
                text_color = text_info[i][1]

                screen.fill(black)
                text = koreanfont.render(current_text, True, text_color)
                text_rect = text.get_rect()
                text_rect.center = (screen_width // 2, screen_height // 2)

                start_time = pygame.time.get_ticks()

            else:
                time.sleep(1)
                storying = False
                
        pygame.display.flip()

def death_story():
    
    #색 정의
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    purple = (148, 0, 211)

    start_time = pygame.time.get_ticks()

    #text정의
    text_info = [
        ["용사가 쓰러졌군요.", white],
        ["하지만 괜찮아요.", white],
        ["다시 일어나 희망의 불씨를 태울테니", purple],
        ["다시하시겠습니까?", white]
        ]

    current_text = text_info[0][0]
    text_color = text_info[0][1]
    text = koreanfont.render(current_text, True, text_color)
    text_rect = text.get_rect()
    text_rect.center = (screen_width // 2, screen_height // 2)#화면 중앙


    screen.fill(black)

    storying = True
    i = 0
    while storying:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                storying = False

        screen.blit(text,text_rect)

        current_time = pygame.time.get_ticks()
        if current_time - start_time >= len(text_info[i][0])*100 + 800:  #여기서 시간을 계산
            i += 1
            if len(text_info) > i:
                current_text = text_info[i][0]
                text_color = text_info[i][1]

                screen.fill(black)
                text = koreanfont.render(current_text, True, text_color)
                text_rect = text.get_rect()
                text_rect.center = (screen_width // 2, screen_height // 2)

                start_time = pygame.time.get_ticks()

            else:
                yes = koreanfont.render("예", True, (0, 255, 0))
                yes_rect = yes.get_rect()
                yes_rect.center = (600, screen_height // 2 +40)
                no = koreanfont.render("아니오", False, red)
                no_rect = no.get_rect()
                no_rect.center = (700, screen_height // 2 +40)
                
                choosing = True
                while choosing:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            choosing = False
                            storying = False

                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                mouseposition = pygame.mouse.get_pos()
                                if yes_rect.collidepoint(mouseposition):
                                    time.sleep(0.5)
                                    start_story()
                                    choosing = False
                                    storying = False
                                elif no_rect.collidepoint(mouseposition):
                                    time.sleep(0.5)
                                    choosing = False
                                    storying = False

                    screen.blit(text, text_rect)
                    screen.blit(yes, yes_rect)
                    screen.blit(no, no_rect)
                    pygame.display.flip()
                
                
                
        pygame.display.flip()
    
start_story()

#todo 앤딩 추가