import pygame
import random
import time
from pyc import *
from pygame.sprite import AbstractGroup

pygame.init() #초기화

koreanfont = pygame.font.SysFont('malgungothic',30) #한글 폰트(맑은고딕)

background_image = pygame.image.load("background.png") #배경이미지
chest_image = pygame.image.load("") #상자이미지

screen_width, screen_height = 1200, 700 #화면 넓이, 높이
screen = pygame.display.set_mode((screen_width, screen_height)) #게임 창 크기
pygame.display.set_caption("김건후") #게임 창 이름
clock = pygame.time.Clock()

enemy_xlocation = [950, 900, 850, 800, 750, 700, 650, 600] #적 x좌표
enemy_ylocation = 350 #적 y좌표

class playerSprite(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.player_image = pygame.image.load(image)
        self.player_position = self.rect.center = position
        self.rect = self.player_image.get_rect()
        self.max_health = self.current_health = 5
        self.max_cost = self.current_cost = 3
        self.critical = 25
        self.defending = 0

    def damaged(self, damage):
        real_damage = 0
        if damage >= self.defending: real_damage = damage - self.defending
        else: self.defending -= damage
        self.current_health -= real_damage

    def canUse(self, cost):
        return self.current_cost >= cost

    def usecost(self, amount):
        self.current_cost -= amount
    
    def health_recover(self, recovering):
        self.current_health += recovering
        if self.current_health > self.max_health: self.current_health = self.max_health
    
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
        images = ['','','','']
        self.enemy_image = pygame.image.load(images[enemy_type - 1])
        self.enemy_position = position
        self.rect = self.enemy_image.get_rect()

        info = [[3,1,0], [5,2,0], [8,3,0], [15,4,3]]
        self.health = info[enemy_type - 1][0]
        self.deal = info[enemy_type - 1][1]
        self.defending = info[enemy_type - 1][2]
        self.enemy_type = enemy_type
        if enemy_type == 4:
            self.skill_turn = 3 #스킬 쿨타임
        

    def update(self, position):
        self.enemy_position = position
        self.rect.center = self.enemy_position
        
    def damaged(self, damage):
        real_damage = damage - self.defending
        self.health -= real_damage
        if self.health > 0: return 1
        else: return 0
    
    def boss_skill(self, enemies):
        enemy = enemySprite(randomEnemy(5,3,2), (enemy_xlocation[len(enemies)], enemy_ylocation))
        enemies.add(enemy)
        self.skill_turn = 3

class cardSprite(pygame.sprite.Sprite):
    def __init__(self, card_type):
        pygame.sprite.Sprite.__init__(self)
        images = ['','','','','','','','','','']
        costs = []
        positions = []
        self.card_image = pygame.image.load(images[card_type - 1])
        self.card_cost = costs[card_type - 1]
        self.card_position = positions[card_type - 1]
        self.rect = self.card_image.get_rect()
        self.card_type = card_type
    
    def useCard(self):
        if playerSprite.canUse(self.card_cost):
            playerSprite.usecost(self.card_cost)
            if self.card_type == 1:
                pass #1번카드 효과
            elif self.card_type == 2:
                pass #2번카드 효과
            elif self.card_type == 3:
                pass #3번카드 효과
            elif self.card_type == 4:
                pass #4번카드 효과
            elif self.card_type == 5:
                pass #5번카드 효과
            elif self.card_type == 6:
                pass #6번카드 효과
            elif self.card_type == 7:
                pass #7번카드 효과
        
        else: 
            message_costscarce = koreanfont.render('코스트가 부족합니다',True, (0,0,0))
            message_costscarce_x = message_costscarce.get_rect()[2]
            screen.blit(message_costscarce, (screen_width/2 - message_costscarce_x/2 , 30))

def randomEnemy(first, second, third):
    li = []
    for _ in range(first): li.append(1)
    for _ in range(second): li.append(2)
    for _ in range(third): li.append(3)
    choiced = random.choice(li)
    return choiced

def makeStage(stage):

    enemies = pygame.sprite.Group()
    if stage == 1:
        for i in range(3):
            enemy = enemySprite(randomEnemy(7,2,1), (enemy_xlocation[i], enemy_ylocation))
            enemies.add(enemy)
    elif stage == 2:
        for i in range(3):
            enemy = enemySprite(randomEnemy(5,3,2), (enemy_xlocation[i], enemy_ylocation))
            enemies.add(enemy)
    elif stage == 3:
        for i in range(5):
            enemy = enemySprite(randomEnemy(5,3,2), (enemy_xlocation[i], enemy_ylocation))
            enemies.add(enemy)
    elif stage == 4:
        enemy = enemySprite(4, (enemy_xlocation[0], enemy_ylocation))
        enemies.add(enemy)
    return enemies

def start_story():
    #색 정의
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    purple = (148, 0, 211)

    screen_width, screen_height = 1200, 700 #화면 넓이, 높이
    screen = pygame.display.set_mode((screen_width, screen_height)) #게임 창 크기

    display_duration = 1000 #1초 (단위:밀리초)
    text_change_delay = 2000
    start_time = pygame.time.get_ticks()

    #text정의
    current_text = "이곳은 새벽의 나라"
    text_color = white
    text = koreanfont.render(current_text, True, white)
    text_rect = text.get_rect()
    text_rect.center = (screen_width // 2, screen_height // 2)#크기

    screen.fill(black)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(text,text_rect)

        current_time = pygame.time.get_ticks()
        if current_time - start_time >= text_change_delay:    #여기서 시간을 계산
            if current_text == "이곳은 새벽의 나라":
                current_text = "다른 나라에 비해 발전은 늦지만"

            elif current_text == "다른 나라에 비해 발전은 늦지만":
                current_text = "높은 인망으로 호평을 받는 곳이다."

            elif current_text == "높은 인망으로 호평을 받는 곳이다.":
                current_text = "그런데"
                text_color = red

            elif current_text == "그런데":
                current_text = "땅이 갈라지며 나타난"
                text_color = white

            elif current_text == "땅이 갈라지며 나타난":
                current_text = "절망의 군대"
                text_color = purple

            elif current_text == "절망의 군대":
                current_text = "그들은 모든 건물을 불태우고 사람들을 죽였다."
                text_color = white

            elif current_text == "그들은 모든 건물을 불태우고 사람들을 죽였다.":
                current_text = "그러나 나라를 구하기 위해 나타난 전사"

            elif current_text == "그러나 나라를 구하기 위해 나타난 전사":
                current_text = "그는 곧장 절망의 미로로 들어갔고"

            elif current_text == "그는 곧장 절망의 미로로 들어갔고":
                current_text = "적을 섬멸해 나간다."

            elif current_text == "적을 섬멸해 나간다.":
                current_text = "그의 이름은 바로..."

            screen.fill(black)
            text = koreanfont.render(current_text, True, text_color)
            text_rect = text.get_rect()
            text_rect.center = (screen_width // 2, screen_height // 2)

            start_time = pygame.time.get_ticks()
                
        pygame.display.flip()

    pygame.quit()

def game_loop():
    player = playerSprite("tempplayer.png", (300, 350)) #class 생성
    player_group = pygame.sprite.RenderPlain(player)

    running = 1 #게임이 실행중인가?
    playerturn = 1 #플레이어 턴인가?
    stage = 1 #스테이지
    enemies = makeStage(stage)
    cards = pygame.sprite.Group()
    while running:
        for event in pygame.event.get(): #이벤트 입력
            if event.type == pygame.QUIT: #X버튼 눌렀을 때
                running = 0 #프로그램 종료
        
        if playerturn:
            selected_card = 0
            mouse_left = pygame.mouse.get_pressed()[0]
            if mouse_left:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for card in cards:
                    if card.rect.collidepoint(mouse_x, mouse_y):
                        card.useCard()
                        if playerSprite.current_cost == 0:
                            playerturn = 0
                        for enemy in enemies:
                            if enemy.health < 0: enemies.remove(enemy)
                        if len(enemies) == 0:
                            chest()
                            stage += 1
                            enemies = makeStage(stage)
                            playerturn = 1

        else:
            for enemy in enemies:
                playerSprite.damaged(enemy.deal)
                time.sleep(0.5)
                if playerSprite.current_health < 0: end()
                if enemy.enemy_type == 4:
                    if enemy.skill_turn == 0: enemy.boss_skill(enemies)
                    else: enemy.skill_turn -= 1
    
        screen.blit(background_image, (0,0)) #배경이미지
        player_group.clear(screen, background_image)
        enemies.clear(screen, background_image)
        cards.clear(screen, background_image)
        player_group.draw(screen)
        enemies.draw(screen)
        cards.draw(screen)

        pygame.display.flip()
        clock.tick(10) #FPS

    pygame.quit() #종료

def chest():


    running = True
    chestcard = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if True: #마우스랑 상자가 닿았는가?
                    chestcard.append() #카드 추가

        

def end():
    running = False
    
if __name__ == "__main__": game_loop()

#todo 코스트가 부족합니다 메세지 지우는 기능 추가
#todo 스테이지 추가
#todo 카드 파트
#todo 카드 효과
#todo 기본 카드 추가
#todo 앤딩 추가
#todo 상자 여는것 추가