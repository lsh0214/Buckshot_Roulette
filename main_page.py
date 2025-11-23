import math
from screeninfo import get_monitors
import pygame
import sys
import webbrowser

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

"""쓸 변수들 정리"""

# GameLobby
GAME_LOBBY_IMG = pygame.image.load("game_lobby_img/GameLobby.png").convert_alpha() #주소 기입 방식 찾아봤음
GAME_LOBBY_IMG = pygame.transform.smoothscale(GAME_LOBBY_IMG, (int(screen_width*1.2),int(screen_height*1.2)))
LOBBY_DOOR_IMG = pygame.image.load("game_lobby_img/lobby_door.png").convert_alpha()

#corridor
CORRIDOR_lightOn_IMG = pygame.image.load("game_lobby_img/corridor_lightOn.png").convert_alpha()
CORRIDOR_lightOn_IMG = pygame.transform.scale(CORRIDOR_lightOn_IMG, (screen_width,screen_height))
CORRIDOR_lightOff_IMG = pygame.image.load("game_lobby_img/corridor_lightOff.png").convert_alpha()
CORRIDOR_lightOff_IMG = pygame.transform.scale(CORRIDOR_lightOff_IMG, (screen_width,screen_height))



WHITE = (192, 192, 192)
L_BLACK = (95,95,95)
BLACK = (0,0,0)
FONT = "Fake Receipt.otf"
LOGO = pygame.image.load('menu_img/Buckshot_logo.png').convert_alpha()
LOGO = pygame.transform.scale(LOGO, (950,750))
KANGNAM_LOGO = pygame.image.load('menu_img/KangnamUniversity.png').convert_alpha()
KANGNAM_LOGO = pygame.transform.scale(KANGNAM_LOGO, (200,200))
MENU_BULLET_IMG_1 = pygame.image.load('menu_img/menu_bullet_img1.png').convert_alpha()
MENU_BULLET_IMG_2 = pygame.image.load('menu_img/menu_bullet_img2.png').convert_alpha()
MENU_SCROLL_SPEED = 5
TIME = pygame.time.Clock()
OUR_LOGO = pygame.image.load('credit_img/our_logo.png').convert_alpha()
OUR_LOGO = pygame.transform.scale(OUR_LOGO, (1000,800))
CREDIT_SCROLL_SPEED = 3

#초기 화면 설정
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
            self.image = pygame.Surface((self.text.get_width(), self.text.get_height()))
            self.image.fill((0, 0, 0))
            
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

# credit_exit_btn = Button(None, screen_width_half, screen_height_half + 670, "EXIT", get_font(80), WHITE, L_BLACK)
# # 위 크래딧 버튼은 후에 또 바꿀 예정

#총알 내려오는 거 홤수화
def scroll_bullet(stop):
    global MENU_BULLET_IMG_1_y_pos, MENU_BULLET_IMG_2_y_pos
    MENU_BULLET_IMG_1_y_pos +=MENU_SCROLL_SPEED
    MENU_BULLET_IMG_2_y_pos +=MENU_SCROLL_SPEED

    if MENU_BULLET_IMG_1_y_pos >=screen_height:
        MENU_BULLET_IMG_1_y_pos = MENU_BULLET_IMG_2_y_pos - screen_height
    if MENU_BULLET_IMG_2_y_pos >=screen_height:
        MENU_BULLET_IMG_2_y_pos = MENU_BULLET_IMG_1_y_pos - screen_height
    if stop:
        return [MENU_BULLET_IMG_1_y_pos, MENU_BULLET_IMG_2_y_pos]

#메뉴 블릿 함수
def menu_blit(mouse_pos):
    screen.fill(BLACK)
    scroll_bullet(0)
    
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

# 페이드 인 아웃 함수
def fade_in():
    return
def fade_out():
    global screen
    screen.fill(BLACK)
    img_positions = scroll_bullet(1)
    for i in range(2):
        if i:
            MENU_BULLET_IMG_2_y_pos = img_positions[i]
        else:
            MENU_BULLET_IMG_1_y_pos = img_positions[i]
    for opacity in range(255,0,-5):
        screen.fill(BLACK)
        MENU_BULLET_IMG_1.set_alpha(opacity)
        MENU_BULLET_IMG_2.set_alpha(opacity)

        screen.blit(MENU_BULLET_IMG_1, (0, MENU_BULLET_IMG_1_y_pos))
        screen.blit(MENU_BULLET_IMG_2, (0, MENU_BULLET_IMG_2_y_pos))
        pygame.display.update()
        pygame.time.delay(20)
    MENU_BULLET_IMG_1.set_alpha(255)
    MENU_BULLET_IMG_2.set_alpha(255)
    return 1

#크래딧에 들어갈 요소랑 기본 위치 세팅
credit_elements = [
        (OUR_LOGO, 0),
        (get_font(50).render("Credits", True, WHITE),900),
        (get_font(50).render("Credits", True, WHITE),980),
        (get_font(50).render("Credits", True, WHITE),1070),
        (get_font(50).render("Credits", True, WHITE),1160),
        (get_font(50).render("Credits", True, WHITE),1250),
        (get_font(50).render("Credits", True, WHITE),1340),
        (get_font(50).render("Credits", True, WHITE),1430),
        (get_font(50).render("Credits", True, WHITE),1520)
]
credits_elements_y_pos = screen_height
max_space = credit_elements[-1][1]

#크래딧 블릿 함수
def credit_blit():
    global state, credits_elements_y_pos
    screen.fill(BLACK)

    for element, space in credit_elements:
        y = credits_elements_y_pos + space
        if isinstance(element, pygame.Surface):
                IMG_size_width = element.get_rect().size[0]
                IMG_x_position = screen_width_half-(IMG_size_width/2)
                screen.blit(element, (IMG_x_position, y))
        else:  # 텍스트일 경우
            TEXT_size_width = element.get_rect().size[0]
            TEXT_x_position = screen_width_half-(TEXT_size_width/2)
            screen.blit(element, (TEXT_x_position, y))
    credits_elements_y_pos -= CREDIT_SCROLL_SPEED
    if credits_elements_y_pos + max_space + 100 < 0:  #여기 들어간 숫자는 폰트 크기에 + 20한 거임.
        state = 'menu'
        credits_elements_y_pos = screen_height



#카메라 함수들 정리
"""
지금 필요한 거 정리
1. 화장실에서 바라보는 문 이미지 불러오고 그 이미지 screen에 맞추기
2. 걸음을 걸을 때 움직이는 카메라 워킹 함수
3. 문 열리고 엑션 단축하기 위해서 이미지 갈아끼면서 재활용 가능한 화면으로
4. 로비에서 카메라가 이리저리 흔들리는 거 표현하자.
"""
#카메라 함수들 정리
shaking_bool = True
shaking_range = 40
# 레미니스케이트 곡선(∞ 모양)을 위한 각도
shake_angle = 0
shake_speed = 0.02  # 회전 속도 (작을수록 느림)

def shaking_camera():
    global shake_angle
    
    if shaking_bool:
        # 레미니스케이트 곡선 (옆으로 누운 8자) 공식
        # x = a * cos(t) / (1 + sin²(t))
        # y = a * sin(t) * cos(t) / (1 + sin²(t))
        
        # 각도 증가
        shake_angle += shake_speed
        
        # 레미니스케이트 곡선 계산
        sin_t = math.sin(shake_angle)
        cos_t = math.cos(shake_angle)
        denominator = 1 + sin_t * sin_t
        
        x = shaking_range * cos_t / denominator
        y = shaking_range * sin_t * cos_t / denominator
        
        return (int(x*1.2), int(y*1.2))
    else:
        return (0, 0)

#게임 로비 필요한 요소들 정리
LOBBY_DOOR_IMG = pygame.transform.smoothscale(LOBBY_DOOR_IMG, (int(0.1981944*screen_width*1.2), int(0.582778*screen_height*1.2)))
# 버튼을 전역으로 선언하지 않고, 함수 내에서 생성
LOBBY_DOOR_btn = Button(LOBBY_DOOR_IMG, int(0.517799*screen_width), int(0.452778*screen_height))

save_shake_offset = (0,0)
# 게임 로비 블릿 함수
def gamelobby_blit(mouse_pos):
    global screen, LOBBY_DOOR_btn, save_shake_offset
    # 흔들림 오프셋 가져오기 (∞ 모양)
    shake_offset = shaking_camera()
    
    screen_setting = (int(shake_offset[0] * 1.2), int(shake_offset[1] * 1.2))

    # 배경 이미지 그리기 (흔들림 적용)
    screen.blit(GAME_LOBBY_IMG, GAME_LOBBY_IMG.get_rect(center=(screen_width_half+screen_setting[0], screen_height_half+screen_setting[1])))
    
    # 버튼 위치 업데이트 (흔들림 적용)
    LOBBY_DOOR_btn.x_pos = int(0.517799 * screen_width * 1.2) + screen_setting[0]
    LOBBY_DOOR_btn.y_pos = int(0.452778 * screen_height * 1.2) + screen_setting[1]
    LOBBY_DOOR_btn.btn_rect = LOBBY_DOOR_btn.image_btn.get_rect(center=(LOBBY_DOOR_btn.x_pos, LOBBY_DOOR_btn.y_pos))
    # 버튼 그리기
    LOBBY_DOOR_btn.check_for_hover(mouse_pos)
    LOBBY_DOOR_btn.update(screen) 

    save_shake_offset = shake_offset


# GameLobby door clicked
GAME_LOBBY_FEETO_IMG = pygame.image.load("game_lobby_img/gameLobby_feetO.png").convert_alpha()
GAME_LOBBY_FEETO_IMG = pygame.transform.scale(GAME_LOBBY_FEETO_IMG, (screen_width,screen_height))

GAME_LOBBY_FEETX_IMG = pygame.image.load("game_lobby_img/gameLobby_feetx.png").convert_alpha()
GAME_LOBBY_FEETX_IMG = pygame.transform.scale(GAME_LOBBY_FEETX_IMG, (screen_width,screen_height))

GAME_LOBBY_OPENDOOR_IMG = pygame.image.load("game_lobby_img/gameLobby_open_door.png").convert_alpha()
GAME_LOBBY_OPENDOOR_IMG = pygame.transform.scale(GAME_LOBBY_OPENDOOR_IMG, (screen_width,screen_height))

GAME_LOBBY_OPENDOOR_VIEW_IMG = pygame.image.load("game_lobby_img/corridor_gameLobby_view.png").convert_alpha()
GAME_LOBBY_OPENDOOR_VIEW_IMG = pygame.transform.scale(GAME_LOBBY_OPENDOOR_VIEW_IMG, (screen_width,screen_height))

#걸어가는 화면 함수
def Walk(num):
    global screen, state, GAME_LOBBY_IMG
    trash_img = GAME_LOBBY_IMG.copy()
    for i in range(1, save_shake_offset[0] + 5):
        for j in range(1, save_shake_offset[1] + 1):
            screen.fill(BLACK)
            screen.blit(trash_img, trash_img.get_rect(center=(screen_width_half - i, screen_height_half - j)))
            pygame.display.update()
            pygame.time.delay(100)
    
    for i in range(1, num + 1):
        screen.fill(BLACK)
        scaled_img = pygame.transform.smoothscale(
            trash_img,
            (int(screen_width * 1.2) + i * 20, int(screen_height * 1.2) + i * 20)
        )
        screen.blit(scaled_img, scaled_img.get_rect(center=(screen_width_half, screen_height_half)))
        pygame.display.update()
        pygame.time.delay(100)
    state= 'corridor'


# # 복도로 가는 장면 함수
# def lobby_to_corridor():
#     Walk(3)

# 복도 블릿 함수
def corridor_blit():
    global state, screen
    screen.blit(CORRIDOR_lightOff_IMG,(0,0))

# --- 메인 게임 루프 ---
def main():
    global state, credits_elements_y_pos, shaking_bool, shake_angle, check_num

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if state == 'credit' or state == 'lobby' or state == 'corridor':
                    state = 'menu'
                    shaking_bool = True
                    shake_angle = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if state == 'menu':
                    if start_btn.check_for_input(mouse_pos):
                        print("시작 버튼 눌림")
                        check_num = fade_out()
                        state = 'lobby'
                        shaking_bool = True
                        shake_angle = 0
                        # 게임 시작 로직 추가
                    elif multi_btn.check_for_input(mouse_pos):
                        print("멀티 버튼 눌림")
                    elif option_btn.check_for_input(mouse_pos):
                        print("옵션 버튼 눌림")
                    elif credit_btn.check_for_input(mouse_pos):
                        print("크레딧 버튼 눌림")
                        fade_out()
                        state = 'credit'
                        credits_elements_y_pos = screen_height
                    elif exit_btn.check_for_input(mouse_pos):
                        print("탈출 버튼 눌림")
                        running = False
                    elif kangnam_link_btn.check_for_input(mouse_pos):
                        webbrowser.open('https://web.kangnam.ac.kr/')
                        
            
                elif state == 'lobby' and LOBBY_DOOR_btn.check_for_input(mouse_pos):
                    shaking_bool = False
                    LOBBY_DOOR_IMG.set_alpha(0)
                    GAME_LOBBY_IMG.set_alpha(0)
                    Walk(3)
        screen.fill(BLACK)
        if state == 'menu':
            menu_blit(mouse_pos)
        elif state == 'credit':
            credit_blit()
        elif state == 'lobby':
            gamelobby_blit(mouse_pos)
        elif state == 'corridor':
            corridor_blit()
        pygame.display.update()
        TIME.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()