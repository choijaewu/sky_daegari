import pygame
import sys

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("마우스 클릭으로 스프라이트 클릭 감지")

# 스프라이트 클래스 정의
class MySprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.num = 1

# 스프라이트 그룹 생성
all_sprites_group = pygame.sprite.Group()

# 빨간색 스프라이트 이미지 생성
sprite_image = pygame.Surface((50, 50))
sprite_image.fill((255, 0, 0))

# 스프라이트 생성
sprite1 = MySprite(sprite_image, 100, 200)
sprite2 = MySprite(sprite_image, 300, 400)

# 스프라이트 그룹에 스프라이트 추가
all_sprites_group.add(sprite1)
all_sprites_group.add(sprite2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 마우스 클릭 이벤트 감지
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            clicked_sprites = [sprite for sprite in all_sprites_group if sprite.rect.collidepoint(mouse_x, mouse_y)]

            # 마우스로 클릭한 스프라이트 출력
            for sprite in clicked_sprites:
                print(f"클릭한 스프라이트 위치: ({sprite.rect.x}, {sprite.rect.y}, {sprite.num})")

    screen.fill((255, 255, 255))

    # 스프라이트 그룹 내의 스프라이트들 그리기
    for sprite in all_sprites_group:
        screen.blit(sprite.image, sprite.rect)

    pygame.display.flip()

pygame.quit()