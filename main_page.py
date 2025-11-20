from screeninfo import get_monitors
import pygame
import sys
import webbrowser

"""쓸 변수들 정리"""
GAME_LOBBY_IMG = "gameLobby.png" #주소 기입 방식 찾아봤음
WHITE = (192, 192, 192)
L_BLACK = (95,95,95)
BLACK = (0,0,0)
FONT = "Fake Receipt.otf"
LOGO = pygame.image.load('Buckshot_logo.png')
LOGO = pygame.transform.scale(LOGO, (950,750))
KANGNAM_LOGO = pygame.image.load('KangnamUniversity.png')
KANGNAM_LOGO = pygame.transform.scale(KANGNAM_LOGO, (200,200))
MENU_BULLET_IMG_1 = pygame.image.load('menu_bullet_img1.png')
MENU_BULLET_IMG_2 = pygame.image.load('menu_bullet_img2.png')
SCROLL_SPEED = 15
TIME = pygame.time.Clock()

"""
초기 설정
"""
pygame.init()

for m in get_monitors():
    if m.is_primary:
        screen_width, screen_height = m.width, m.height
        break
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
screen_height_half = screen_height/2
screen_width_half = screen_width/2

state = 'menu'


#기본 폰트 함수
def get_font(size):
    return pygame.font.Font(FONT, size)

#커서 모양 바꾸기 함수
def mouse_cursor_hand():
    return pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
def mouse_cursor_arrow():
    return pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

#버튼 클래스
class Button():
    """
    텍스트 버튼을 위한 재사용 가능한 클래스
    """
    def __init__(self, image_btn, x, y, text_input=None, font=None, base_color=None, hovering_color=None):
        # 1. 버튼 기본 속성 설정
        self.image_btn = image_btn

        self.x_pos = x
        self.y_pos = y
        self.font = font
        self.base_color = base_color       # 기본 텍스트 색
        self.hovering_color = hovering_color # 마우스 올렸을 때 텍스트 색
        
        # 2. 텍스트 렌더링
        if text_input is not None:
            self.text_input = text_input
            self.text = self.font.render(self.text_input, True, self.base_color)
            # 3. 버튼 사각형(rect) 만들기
            # 텍스트 이미지의 rect를 가져옴
            self.image = self.text 
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
            # 4. 현재 텍스트 (마우스 오버 효과를 위해)
            self.text_surface = self.text
        else:
            self.btn_rect = self.image_btn.get_rect(center=(self.x_pos, self.y_pos))
        
        

    def update(self, screen):
        """
        매 프레임마다 버튼을 화면에 그립니다.
        """
        if self.image_btn is not None:
            screen.blit(self.image_btn, self.btn_rect)
        else:
            screen.blit(self.text_surface, self.rect)

    def check_for_input(self, position):
        """
        마우스 클릭 이벤트를 확인합니다. (위치만 확인)
        position: pygame.mouse.get_pos() 값
        """
        if self.image_btn is None:
            if position[0] in range(self.rect.left, self.rect.right) and \
                position[1] in range(self.rect.top, self.rect.bottom):
                return True # 버튼 안에서 클릭됨
        elif self.image_btn is not None:
            if position[0] in range(self.btn_rect.left, self.btn_rect.right) and \
                position[1] in range(self.btn_rect.top, self.btn_rect.bottom):
                return True # 버튼 안에서 클릭됨
        
        return False

    def check_for_hover(self, position):
        """
        마우스 호버(Hover) 효과를 적용합니다. (색상 변경)
        position: pygame.mouse.get_pos() 값
        """
        if self.image_btn is None:
            if position[0] in range(self.rect.left, self.rect.right) and \
            position[1] in range(self.rect.top, self.rect.bottom):
                self.text_surface = self.font.render(self.text_input, True, self.hovering_color)
                
            else:
                self.text_surface = self.font.render(self.text_input, True, self.base_color)
                
        else:
            if position[0] in range(self.btn_rect.left, self.btn_rect.right) and \
            position[1] in range(self.btn_rect.top, self.btn_rect.bottom):
                mouse_cursor_hand()
            else:
                mouse_cursor_arrow()
#스크롤 위치 세팅
MENU_BULLET_IMG_1 = pygame.transform.scale(MENU_BULLET_IMG_1, (screen_width,screen_height))
MENU_BULLET_IMG_2 = pygame.transform.scale(MENU_BULLET_IMG_2, (screen_width,screen_height))

MENU_BULLET_IMG_1_y_pos = 0
MENU_BULLET_IMG_2_y_pos = screen_height

#버튼 세팅
start_btn = Button(None, screen_width_half, screen_height_half + 350, "START", get_font(80), WHITE, L_BLACK)
multi_btn = Button(None, screen_width_half, screen_height_half + 430, "MULTIPLAY", get_font(80), WHITE, L_BLACK)
option_btn = Button(None, screen_width_half, screen_height_half + 510, "OPTIONS", get_font(80), WHITE, L_BLACK)
credit_btn = Button(None, screen_width_half, screen_height_half + 590, "CREDITS", get_font(80), WHITE, L_BLACK)
exit_btn = Button(None, screen_width_half, screen_height_half + 670, "EXIT", get_font(80), WHITE, L_BLACK)
kangnam_link_btn = Button(KANGNAM_LOGO, screen_width - 200 + 100, screen_height - 200 + 100)

menu_buttons = [start_btn, multi_btn, option_btn, credit_btn, exit_btn, kangnam_link_btn]

credit_exit_btn = Button(None, screen_width_half, screen_height_half + 670, "EXIT", get_font(80), WHITE, L_BLACK)
# 위 크래딧 버튼은 후에 또 바꿀 예정

#총알 내려오는 거 홤수화
def scroll_bullet():
    global MENU_BULLET_IMG_1_y_pos, MENU_BULLET_IMG_2_y_pos
    MENU_BULLET_IMG_1_y_pos +=SCROLL_SPEED
    MENU_BULLET_IMG_2_y_pos +=SCROLL_SPEED

    if MENU_BULLET_IMG_1_y_pos >=screen_height:
        MENU_BULLET_IMG_1_y_pos = MENU_BULLET_IMG_2_y_pos - screen_height
    if MENU_BULLET_IMG_2_y_pos >=screen_height:
        MENU_BULLET_IMG_2_y_pos = MENU_BULLET_IMG_1_y_pos - screen_height

#메뉴 블릿 함수
def menu_blit(mouse_pos):
    screen.fill(BLACK)
    scroll_bullet()
    
    #버전 텍스트
    txt = get_font(40)
    version_txt = txt.render('0.0.1(Prototype)', True, L_BLACK)

    #로고 이미지
    LOGO_size_width = LOGO.get_rect().size[0]
    LOGO_x_position = screen_width_half-(LOGO_size_width/2)

    #blit 모음
    screen.blit(LOGO, (LOGO_x_position, 250))
    screen.blit(MENU_BULLET_IMG_1, (0, MENU_BULLET_IMG_1_y_pos))
    screen.blit(MENU_BULLET_IMG_2, (0, MENU_BULLET_IMG_2_y_pos))
    screen.blit(version_txt,(30, screen_height - 80))

    for btn in menu_buttons:
        btn.check_for_hover(mouse_pos)
        btn.update(screen)

#크래딧 블릿 함수
def credit_blit(mouse_pos):
    text_font = get_font(50)
    credit_text = text_font.render("Credits", True, WHITE)
    credit_rect = credit_text.get_rect(center=(screen_width_half, screen_height_half - 100))
    screen.blit(credit_text, credit_rect)

    credit_exit_btn.check_for_hover(mouse_pos)
    credit_exit_btn.update(screen)

# --- 메인 게임 루프 ---
def main():
    global state

    running = True
    while running:
        TIME.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if state == 'menu':
                    if start_btn.check_for_input(mouse_pos):
                        print("시작 버튼 눌림")
                        # 게임 시작 로직 추가
                    elif multi_btn.check_for_input(mouse_pos):
                        print("멀티 버튼 눌림")
                    elif option_btn.check_for_input(mouse_pos):
                        print("옵션 버튼 눌림")
                    elif credit_btn.check_for_input(mouse_pos):
                        print("크레딧 버튼 눌림")
                        state = "credit"
                    elif exit_btn.check_for_input(mouse_pos):
                        print("탈출 버튼 눌림")
                        running = False
                    elif kangnam_link_btn.check_for_input(mouse_pos):
                        webbrowser.open('https://web.kangnam.ac.kr/')
                elif state == "credit":
                    if credit_exit_btn.check_for_input(mouse_pos):
                        print("크레딧 탈출 버튼 눌림")
                        state = "menu"
        if state == 'menu':
            menu_blit(mouse_pos)
        elif state == 'credit':
            credit_blit(mouse_pos)
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()