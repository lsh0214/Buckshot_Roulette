import math
from screeninfo import get_monitors
import pygame
import sys
import webbrowser
import lsj_r
import B_def

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
# [최적화 1] 배경 이미지는 투명도가 필요 없으므로 convert()를 사용하여 렌더링 속도 향상
GAME_LOBBY_IMG = pygame.image.load("game_lobby_imgs/GameLobby.png").convert() 



WHITE = (192, 192, 192)
L_BLACK = (95,95,95)
BLACK = (0,0,0)
FONT = "Fake Receipt.otf"
LOGO = pygame.image.load('menu_imgs/Buckshot_logo.png').convert_alpha()
LOGO = pygame.transform.scale(LOGO, (int(screen_width* 0.330),int(screen_height*0.417)))
KANGNAM_LOGO = pygame.image.load('menu_imgs/KangnamUniversity.png').convert_alpha()
KANGNAM_LOGO = pygame.transform.scale(KANGNAM_LOGO, (int(screen_width  * 0.0694),int(screen_height * 0.1111)))
kangnam_logo_x = int(screen_width  * 0.0694)
kangnam_logo_y = int(screen_height  * 0.1111)
MENU_BULLET_IMG_1 = pygame.image.load('menu_imgs/menu_bullet_img1.png').convert_alpha()
MENU_BULLET_IMG_2 = pygame.image.load('menu_imgs/menu_bullet_img2.png').convert_alpha()
MENU_SCROLL_SPEED = 5
TIME = pygame.time.Clock()
OUR_LOGO = pygame.image.load('credit_imgs/our_logo.png').convert_alpha()
OUR_LOGO = pygame.transform.scale(OUR_LOGO, (int(screen_width*0.347),int(screen_height*0.464)))
CREDIT_SCROLL_SPEED = 3

#초기 화면 설정
state = 'menu'

BASE_WIDTH, BASE_HEIGHT = 2880, 1800  # 기준 해상도, height은 나중에 봐서 버리자

#기본 폰트 함수
def get_font(size):
    scale = screen_width / BASE_WIDTH  # 또는 height 기준으로 해도 됨
    scaled_size = int(size * scale)
    return pygame.font.Font(FONT, scaled_size)

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

#로고 이미지
LOGO_size_width = LOGO.get_rect().size[0]
LOGO_size_height = LOGO.get_rect().size[1]
LOGO_x_position = screen_width_half-(LOGO_size_width/2)
LOGO_y_position = int(screen_height * 0.13)

# LOGO 위치 계산 후
LOGO_rect = LOGO.get_rect()
LOGO_rect.topleft = (LOGO_x_position, LOGO_y_position)
logo_bottom = LOGO_rect.bottom

# 비율로 간격 정의
FIRST_OFFSET_RATIO = 0.12   # LOGO 아래 첫 버튼까지 거리 (screen_height의 15%)
GAP_RATIO          = 0.05   # 버튼 사이 간격 (screen_height의 6%)

first_btn_y = logo_bottom + int(screen_height * FIRST_OFFSET_RATIO)
gap        = int(screen_height * GAP_RATIO)

start_btn  = Button(None, screen_width_half, first_btn_y + 0 * gap, "START",     get_font(80), WHITE, L_BLACK)
multi_btn  = Button(None, screen_width_half, first_btn_y + 1 * gap, "MULTIPLAY", get_font(80), WHITE, L_BLACK)
option_btn = Button(None, screen_width_half, first_btn_y + 2 * gap, "OPTIONS",   get_font(80), WHITE, L_BLACK)
credit_btn = Button(None, screen_width_half, first_btn_y + 3 * gap, "CREDITS",   get_font(80), WHITE, L_BLACK)
exit_btn   = Button(None, screen_width_half, first_btn_y + 4 * gap, "EXIT",      get_font(80), WHITE, L_BLACK)

kangnam_link_btn = Button(KANGNAM_LOGO, screen_width -kangnam_logo_x/2, screen_height -kangnam_logo_y/2)

menu_buttons = [start_btn, multi_btn, option_btn, credit_btn, exit_btn, kangnam_link_btn]

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
    txt_x = version_txt.get_rect().size[0]
    txt_y = version_txt.get_rect().size[1]
    
    #blit 모음
    screen.blit(LOGO, (LOGO_x_position, LOGO_y_position))
    screen.blit(MENU_BULLET_IMG_1, (0, MENU_BULLET_IMG_1_y_pos))
    screen.blit(MENU_BULLET_IMG_2, (0, MENU_BULLET_IMG_2_y_pos))

    screen.blit(version_txt,(20, screen_height - txt_y - 10))

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
shaking_bool = True
shaking_range = 40
# 레미니스케이트 곡선(∞ 모양)을 위한 각도
shake_angle = 0

def shaking_camera(shake_speed, width_range, height_range):
    global shake_angle
    
    if shaking_bool:
        # 레미니스케이트 곡선 (옆으로 누운 8자) 공식
        shake_angle += shake_speed
        sin_t = math.sin(shake_angle)
        cos_t = math.cos(shake_angle)
        denominator = 1 + sin_t * sin_t
        
        x = shaking_range * width_range * cos_t / denominator
        y = shaking_range * height_range * sin_t * cos_t / denominator
        
        return [int(x), int(y)]
    else:
        return (0, 0)
    
GAME_LOBBY_IMG_copy = pygame.transform.smoothscale(GAME_LOBBY_IMG, (int(screen_width*1.2),int(screen_height*1.2)))
LOBBY_DOOR_IMG = pygame.image.load("game_lobby_imgs/lobby_door.png").convert_alpha()

#게임 로비 필요한 요소들 정리
LOBBY_DOOR_IMG = pygame.transform.smoothscale(LOBBY_DOOR_IMG, (int(0.1900944*screen_width*1.2), int(0.543678*screen_height*1.2)))
# 버튼을 전역으로 선언하지 않고, 함수 내에서 생성
LOBBY_DOOR_IMG.set_alpha(0)
LOBBY_DOOR_btn = Button(LOBBY_DOOR_IMG, int(0.525000*screen_width), int(0.432778*screen_height))

save_shake_offset = (0,0)
# 게임 로비 블릿 함수
def gamelobby_blit(mouse_pos):
    global screen, LOBBY_DOOR_btn, save_shake_offset
    # 흔들림 오프셋 가져오기 (∞ 모양)
    shake_speed = 0.03
    shake_offset = shaking_camera(shake_speed, 1, 1)
    shake_offset[0] = shake_offset[0]
    shake_offset[1] = shake_offset[1]

    
    screen_setting = (int(shake_offset[0] * 1.2), int(shake_offset[1] * 1.2))

    # 배경 이미지 그리기 (흔들림 적용)
    screen.blit(GAME_LOBBY_IMG_copy, GAME_LOBBY_IMG_copy.get_rect(center=(screen_width_half+screen_setting[0], screen_height_half+screen_setting[1])))
    
    # 버튼 위치 업데이트 (흔들림 적용)
    LOBBY_DOOR_btn.x_pos = int(0.525000 * screen_width * 1.2) + screen_setting[0]
    LOBBY_DOOR_btn.y_pos = int(0.432778 * screen_height * 1.2) + screen_setting[1]
    LOBBY_DOOR_btn.btn_rect = LOBBY_DOOR_btn.image_btn.get_rect(center=(LOBBY_DOOR_btn.x_pos, LOBBY_DOOR_btn.y_pos))
    # 버튼 그리기
    LOBBY_DOOR_btn.check_for_hover(mouse_pos)
    LOBBY_DOOR_btn.update(screen) 

    save_shake_offset = shake_offset

# GameLobby door clicked
GAME_LOBBY_FEETO_IMG = pygame.image.load("game_lobby_imgs/gameLobby_feetO.png").convert_alpha()
GAME_LOBBY_FEETX_IMG = pygame.image.load("game_lobby_imgs/gameLobby_feetx.png").convert_alpha()
GAME_LOBBY_OPENDOOR_IMG = pygame.image.load("game_lobby_imgs/gameLobby_open_door.png").convert_alpha()
GAME_LOBBY_OPENDOOR_VIEW_IMG = pygame.image.load("game_lobby_imgs/corridor_gameLobby_view.png").convert_alpha()

# --- 변수 선언부에 추가 ---
walk_scale = 1.2
walk_tick = 0.0
walk_drift_x = 0.0    # <--- 추가: 화면의 가로 이동 거리를 저장할 변수
kick_timer = 0
walk_angle = 0.0
IS_WALKING = False
seq_angle = 0
# --- 기존 변수들 아래에 추가 ---
corridor_scale = 1.0
corridor_tick = 0.0
corridor_walk_speed = 0.05  # 복도에서 걸어가는 속도

def lobby_walk():
    global screen, state, walk_scale, walk_tick, walk_drift_x, walk_angle, kick_timer, IS_WALKING, seq_angle
    global GAME_LOBBY_IMG, GAME_LOBBY_FEETX_IMG, GAME_LOBBY_FEETO_IMG, GAME_LOBBY_OPENDOOR_IMG, GAME_LOBBY_OPENDOOR_VIEW_IMG

    # --- [설정값 분리] ---
    
    # [해상도 대응] 이미지 원본 크기 기준
    img_w = GAME_LOBBY_IMG.get_width()
    img_h = GAME_LOBBY_IMG.get_height()

    # 1. 걷기 모드 설정
    WALK_BOB_SPEED = 0.2        
    ZOOM_SPEED = 0.01           
    
    # [비율 수정] 이동 속도를 이미지 너비 비례(%)로 설정하여 모든 해상도에서 동일하게 보이게 함
    # -0.003은 너비의 0.3%만큼 이동
    MOVE_SPEED_RATIO = -0.003

    # --- [단계 1] 걷기 모드 (로비 줌인) ---
    if walk_scale <= 2.5:
        # 타이머 업데이트
        walk_tick += WALK_BOB_SPEED
        # 값 업데이트
        walk_scale += ZOOM_SPEED
        
        # [비율 수정] 픽셀 단위 이동 대신 비율 이동 누적
        walk_drift_x += (img_w * MOVE_SPEED_RATIO)
        
        # [비율 수정] 걷기용 흔들림 (Head Bobbing) - 이미지 크기 비례
        # offset_y: 높이의 약 5% / sway_x: 너비의 약 2%
        walk_offset_y = math.sin(walk_tick) * (img_h * 0.05)
        walk_sway_x = math.cos(walk_tick / 2) * (img_w * 0.02)

        # [핵심 최적화: Crop & Scale 방식]
        # ***중요***: 뷰포트 크기를 '화면 해상도(screen_width)'가 아닌 '원본 이미지(img_w)' 기준으로 계산해야 함
        # 그래야 해상도가 다른 모니터에서도 "이미지의 절반을 자른다"는 비율이 유지됨
        
        view_width = img_w / walk_scale
        view_height = img_h / walk_scale

        # 중심점 계산 (이미지 기준 중앙 + 이동 + 흔들림)
        center_x = (img_w / 2) - ((walk_drift_x + walk_sway_x) / walk_scale)
        center_y = (img_h / 2) - (walk_offset_y / walk_scale)

        # 3. 잘라낼 영역(Rect)의 좌상단 좌표 계산
        crop_x = center_x - (view_width / 2)
        crop_y = center_y - (view_height / 2)

        # 4. 이미지 범위를 벗어나지 않도록 보정
        crop_x = max(0, min(crop_x, img_w - view_width))
        crop_y = max(0, min(crop_y, img_h - view_height))

        # 5. 자르기 (Subsurface) & 현재 모니터 크기로 확대 (Scale)
        try:
            sub_surface = GAME_LOBBY_IMG.subsurface((int(crop_x), int(crop_y), int(view_width), int(view_height)))
            final_img = pygame.transform.scale(sub_surface, (screen_width, screen_height))
            screen.blit(final_img, (0, 0))
        except ValueError:
            pass

    # --- [단계 2] 발차기 시퀀스 ---
    else:
        kick_timer += 1
        # 시퀀스 공통 설정
        seq_scale = 1.2
        seq_width = int(screen_width * seq_scale)
        seq_height = int(screen_height * seq_scale)
        current_img = None
        # 각 단계별 로직 (여기서 duration과 progress를 개별적으로 다시 계산합니다)
        # [0단계: 대기]
        if kick_timer < 5:
            current_img = GAME_LOBBY_FEETX_IMG
            DURATION = 5
            progress = kick_timer / DURATION
            seq_offset_y = 0
            seq_sway_x = 0
        # [1단계: 쾅!]
        elif kick_timer < 10: # 25 + 20프레임
            current_img = GAME_LOBBY_FEETO_IMG
            DURATION = 5
            local_timer = kick_timer - 25
            progress = local_timer / DURATION
            seq_offset_y = math.sin(progress * 2 * math.pi) * -100
            seq_sway_x = math.cos(progress * 2 * math.pi) * 5
        # [2단계: 문 열림]
        elif kick_timer < 15: # 45 + 20프레임
            current_img = GAME_LOBBY_OPENDOOR_IMG
            DURATION = 15
            local_timer = kick_timer - 45
            progress = local_timer / DURATION

            # 문 열릴 때 반동으로 다시 위로 살짝 듬
            seq_offset_y = math.sin(progress * 2 * math.pi) * 100
            seq_sway_x = 0
        # [3단계: 복도 뷰]
        elif kick_timer < 30: # 65 + 60프레임 (여유롭게)
            current_img = GAME_LOBBY_OPENDOOR_VIEW_IMG
            DURATION = 30
            local_timer = kick_timer - 50
            progress = local_timer / DURATION # 0.0 ~ 1.0
            
            seq_offset_y = 0
            
            look_right_amount = progress * 400 
            seq_sway_x = -look_right_amount
        else:
            state = 'corridor'
            IS_WALKING = False
            
            # 복도 애니메이션 초기화 (중요)
            global corridor_scale, corridor_tick
            corridor_scale = 1.0 
            corridor_tick = 0.0
            
            # 이전 상태 변수 초기화
            walk_scale = 1.2
            walk_tick = 0.0
            walk_drift_x = 0.0
            walk_angle = 0.0
            kick_timer = 0
            return
        if current_img:
            scaled_seq_img = pygame.transform.scale(current_img, (seq_width, seq_height))
            seq_rect = scaled_seq_img.get_rect()
            # 위치 적용
            seq_rect.center = (screen_width_half + seq_sway_x, screen_height_half + seq_offset_y)
    
            screen.blit(scaled_seq_img, seq_rect)

#corridor
CORRIDOR_lightOn_IMG = pygame.image.load("game_lobby_imgs/corridor_lightOn.png").convert_alpha()
CORRIDOR_lightOn_IMG = pygame.transform.scale(CORRIDOR_lightOn_IMG, (screen_width,screen_height))
CORRIDOR_lightOff_IMG = pygame.image.load("game_lobby_imgs/corridor_lightOff.png").convert_alpha()
CORRIDOR_lightOff_IMG = pygame.transform.scale(CORRIDOR_lightOff_IMG, (screen_width,screen_height))

#게임 로비 필요한 요소들 정리
CORRIDOR_DOOR_IMG = pygame.image.load("game_lobby_imgs/corridor_door.png").convert_alpha()
CORRIDOR_DOOR_IMG = pygame.transform.smoothscale(CORRIDOR_DOOR_IMG, (int(0.1430556*screen_width),int(0.2572222*screen_height)))
# 버튼을 전역으로 선언하지 않고, 함수 내에서 생성
CORRIDOR_DOOR_IMG.set_alpha(0)
CORRIDOR_DOOR_btn = Button(CORRIDOR_DOOR_IMG, int(0.1*screen_width), int(0.4675*screen_height))

SEE_GAMEROOM_DOOR_IMG = pygame.image.load("game_lobby_imgs/see_gameRoom_door.png").convert_alpha()
SEE_GAMEROOM_DOOR_IMG = pygame.transform.scale(SEE_GAMEROOM_DOOR_IMG, (screen_width,screen_height))

ADD_CORRIDOR_IMG = pygame.image.load("game_lobby_imgs/add_corridor_img.png").convert_alpha()
ADD_CORRIDOR_IMG = pygame.transform.scale(ADD_CORRIDOR_IMG, (screen_width,screen_height))



FLICKER_SPEED = 10

# 복도 블릿 함수
def corridor_blit(mouse_pos):
    global state, screen, corridor_scale, corridor_tick, CORRIDOR_lightOn_IMG
    corridor_tick += 0.1  # 걸음 속도 (박자)
    flicker_value = math.sin(corridor_tick)
    
    # 1. 바닥 배경 (빈공간 방지)
    screen.blit(ADD_CORRIDOR_IMG, ADD_CORRIDOR_IMG.get_rect(center = (screen_width_half, screen_height_half)))

    # 2. 움직이는 배경
    # 깜빡임에 따라 이미지 선택
    if flicker_value > 0.5 or flicker_value<0 and flicker_value>-0.5:
        target_img = CORRIDOR_lightOn_IMG
    else:
        target_img = CORRIDOR_lightOff_IMG
    
    screen.blit(target_img, target_img.get_rect(center = (screen_width_half, screen_height_half)))

    CORRIDOR_DOOR_btn.btn_rect = CORRIDOR_DOOR_btn.image_btn.get_rect(center=(CORRIDOR_DOOR_btn.x_pos, CORRIDOR_DOOR_btn.y_pos))
    # 버튼 그리기
    CORRIDOR_DOOR_btn.check_for_hover(mouse_pos)
    CORRIDOR_DOOR_btn.update(screen) 

    return flicker_value

GAMEROOM_FEETO_IMG = pygame.image.load("game_lobby_imgs/gameroom_feetO.png").convert_alpha()
GAMEROOM_FEETX_IMG = pygame.image.load("game_lobby_imgs/gameroom_feetX.png").convert_alpha()
GAMEROOM_DOOR_OPEN_IMG = pygame.image.load("game_lobby_imgs/gameroom_door_open.png").convert_alpha()
GAMEROOM_VIEW_IMG = pygame.image.load("game_lobby_imgs/gameroom_view.png").convert_alpha()

def corridor_walk(flicker_value, mouse_pos):
    global state, screen, corridor_scale, corridor_tick, CORRIDOR_lightOn_IMG, CORRIDOR_lightOff_IMG, kick_timer
    
    # 1. 걷는 단계 (줌인) - Crop & Scale 최적화 적용
    if corridor_scale <= 3.0:
        # 박자 업데이트 (LobbyWalk와 비슷하게 맞춤)
        WALK_BOB_SPEED = 0.6
        corridor_tick += WALK_BOB_SPEED

        # 배경 벽 (옆으로 지나가는 효과)
        if flicker_value > 0.5 or flicker_value<0 and flicker_value>-0.5:
            current_img = CORRIDOR_lightOn_IMG
        else:
            current_img = CORRIDOR_lightOff_IMG
        
        # 배경 벽은 화면 크기로 고정하고 위치만 이동 (스케일링 X)
        # current_img는 이미 init에서 scale 되어 있음
        current_img_x_pos = screen_width_half + corridor_tick*80 # 이동 속도 조절
        screen.blit(current_img, current_img.get_rect(center = (current_img_x_pos, screen_height_half)))
        
        # 줌 속도
        ZOOM_SPEED = 0.07
        corridor_scale += ZOOM_SPEED
        
        # Head Bobbing (걸을 때 흔들림)
        offset_y = math.sin(corridor_tick) * 80
        offset_x = math.cos(corridor_tick / 2) * 30
            
        # [핵심 최적화: Crop & Scale]
        # SEE_GAMEROOM_DOOR_IMG를 타겟으로 줌인
        
        view_width = screen_width / corridor_scale
        view_height = screen_height / corridor_scale

        # 중앙점 계산 (흔들림 반영)
        center_x = (screen_width / 2) - (offset_x / corridor_scale)
        center_y = (screen_height / 2) - (offset_y / corridor_scale)

        # Crop 영역 계산
        crop_x = center_x - (view_width / 2)
        crop_y = center_y - (view_height / 2)

        # 범위 제한 (IndexError 방지)
        max_x = SEE_GAMEROOM_DOOR_IMG.get_width() - view_width
        max_y = SEE_GAMEROOM_DOOR_IMG.get_height() - view_height
        
        crop_x = max(0, min(crop_x, max_x))
        crop_y = max(0, min(crop_y, max_y))

        try:
            # 원본에서 필요한 부분만 잘라냄 (매우 빠름)
            sub_surface = SEE_GAMEROOM_DOOR_IMG.subsurface((crop_x, crop_y, view_width, view_height))
            # 화면 크기로 확대 (부하 적음)
            final_img = pygame.transform.scale(sub_surface, (screen_width, screen_height))
            screen.blit(final_img, (0, 0))
        except ValueError:
            pass
    
    # 2. 문 여는 시퀀스
    else: 
        kick_timer += 1
        
        # 시퀀스 변수
        seq_scale = 1.2
        seq_width = int(screen_width * seq_scale)
        seq_height = int(screen_height * seq_scale)
        seq_offset_y = 0
        seq_sway_x = 0
        
        current_img = None
        
        # 타이밍을 LobbyWalk 처럼 빠르게 조정 (기존 35, 65... -> 10, 20...)
        # [0단계: 대기]
        if kick_timer < 10:
            current_img = GAMEROOM_FEETX_IMG
            DURATION = 10
            progress = kick_timer / DURATION
            seq_offset_y = 0
            seq_sway_x = 0
        # [1단계: 쾅!]
        elif kick_timer < 20: 
            current_img = GAMEROOM_FEETO_IMG
            DURATION = 15
            local_timer = kick_timer - 10
            progress = local_timer / DURATION
            seq_offset_y = math.sin(progress * 2 * math.pi) * -100
            seq_sway_x = math.cos(progress * 2 * math.pi) * 5
        # [2단계: 문 열림]
        elif kick_timer < 35: 
            current_img = GAMEROOM_DOOR_OPEN_IMG
            DURATION = 15
            local_timer = kick_timer - 20
            progress = local_timer / DURATION

            seq_offset_y = math.sin(progress * 2 * math.pi) * 100
            seq_sway_x = 0
        # [3단계: 복도 뷰]
        elif kick_timer < 50: 
            current_img = GAMEROOM_VIEW_IMG
            DURATION = 50
            local_timer = kick_timer - 30
            progress = local_timer / DURATION
            # 기본 꿀렁임
            seq_offset_y = math.sin(progress * 2 * math.pi) * -100
            seq_sway_x = math.cos(progress * 2 * math.pi) * 5
            # [시선 이동 로직]
            look_right_amount = progress
            seq_sway_x -= look_right_amount
        else:
            global sign_tick  # sign_tick을 제어하기 위해 global 선언 필요
        
            state = 'sign'    # 상태 변경
            sign_tick = 0     # 애니메이션 타이머 초기화 (중요: 재시작 시 버그 방지)
            
            # 빈 화면 방지: 상태가 바뀌자마자 첫 프레임을 즉시 그립니다.
            Sign_blit(mouse_pos)      
            return
            
        # 이미지 그리기
        if current_img:
            scaled_seq_img = pygame.transform.scale(current_img, (seq_width, seq_height))
            seq_rect = scaled_seq_img.get_rect()
            # 위치 적용
            seq_rect.center = (screen_width_half + seq_sway_x, screen_height_half + seq_offset_y)
    
            screen.blit(scaled_seq_img, seq_rect)

#동의서 이미지 로드
GAMEROOM_DEALER_FACE_1 = pygame.image.load("sign_imgs/gameroom_dealer_face_1.png").convert_alpha()
GAMEROOM_DEALER_FACE_2 = pygame.image.load("sign_imgs/gameroom_dealer_face_2.png").convert_alpha()
GAMEROOM_DEALER_FACE_3 = pygame.image.load("sign_imgs/gameroom_dealer_face_3.png").convert_alpha()
GAMEROOM_DEALER_HAND_O = pygame.image.load("sign_imgs/gameroom_dealer_handO.png").convert_alpha()
GAMEROOM_DEALER_HAND_X = pygame.image.load("sign_imgs/gameroom_dealer_handX.png").convert_alpha()
GAMEROOM_DEALER_HAND_CROOK = pygame.image.load("sign_imgs/gameroom_dealer_hand_crook.png").convert_alpha()
GAMEROOM_DEALER_HAND_CROOK_ON_TABLE = pygame.image.load("sign_imgs/gameroom_dealer_hand_crookOntable.png").convert_alpha()
WAIVER_ON_HAND = pygame.image.load("sign_imgs/waiver_onhand_img.png").convert_alpha()
WAIVER_ON_TABLE = pygame.image.load("sign_imgs/waiver_ontable_img.png").convert_alpha()
SEE_WAIVER_VIEW = pygame.image.load("sign_imgs/see_waiver_no.png").convert_alpha()

sign_tick = 0
img = None
current_tick = 0
angle = 0
imgs_not = [GAMEROOM_DEALER_FACE_1, GAMEROOM_DEALER_FACE_2]

#게임 로비 필요한 요소들 정리
WAIVER_ON_TABLE_btn_img = pygame.transform.smoothscale(WAIVER_ON_TABLE, (int(0.13993*screen_width),int(0.18778*screen_height)))
# 버튼을 전역으로 선언하지 않고, 함수 내에서 생성
WAIVER_ON_TABLE_btn = Button(WAIVER_ON_TABLE_btn_img, int(0.44097*screen_width), int(0.19944*screen_height))
#게임 동의서 사인 블릿 함수
def Sign_blit(mouse_pos):
    global state, screen, sign_tick, img, angle, SEE_WAIVER_VIEW
    seq_sway_x = 0
    seq_offset_y = 0
    sign_tick += 1
    
    # --- 1. 이미지 선택 (애니메이션 프레임 변경) ---
    # 여기서는 이미지만 교체하고, 확대 비율 계산에는 관여하지 않습니다.
    if sign_tick <= 10:
        img = GAMEROOM_DEALER_HAND_O
        DURATION = 10
        local_timer = sign_tick - 0
        progress = local_timer / DURATION
        seq_offset_y = -math.sin(progress * math.pi) * 20
    elif sign_tick <= 20:
        img = GAMEROOM_DEALER_HAND_CROOK
        DURATION = 10
        local_timer = sign_tick - 10
        progress = local_timer / DURATION
        seq_offset_y = -math.sin(progress * math.pi) * 15
    elif sign_tick <= 30:
        img = GAMEROOM_DEALER_HAND_CROOK_ON_TABLE
        DURATION = 10
        local_timer = sign_tick - 20
        progress = local_timer / DURATION
        seq_offset_y = -math.sin(progress * math.pi) * 10
    elif sign_tick <= 40:
        img = GAMEROOM_DEALER_FACE_1
    elif sign_tick <= 50:
        img = GAMEROOM_DEALER_FACE_2
    elif sign_tick <= 200:
        img = GAMEROOM_DEALER_FACE_3
        DURATION = 10
        local_timer = sign_tick - 20
        progress = local_timer / DURATION
        seq_offset_y = -math.sin(progress * math.pi) * 10
    elif sign_tick <= 205:
        img = GAMEROOM_DEALER_FACE_3
        DURATION = 5
        local_timer = sign_tick - 20
        progress = local_timer / DURATION
        seq_offset_y = math.sin(progress * math.pi) * -100

    
    # --- 2. 연속적인 줌 인 (Continuous Zoom) ---
    if img:
        if img in imgs_not:
            start_scale = 1.0
            end_scale = 1.2 
            
            current_scale = start_scale + (end_scale - start_scale)
            
            # --- 3. 렌더링 (짝수 보정 & smoothscale 유지) ---
            target_w = int(screen_width * current_scale)
            target_h = int(screen_height * current_scale)

            scale_img = pygame.transform.smoothscale(img, (target_w, target_h))
            rect = scale_img.get_rect()
            rect.center = (screen_width_half + seq_sway_x, screen_height_half + seq_offset_y)
        elif img == GAMEROOM_DEALER_FACE_3 and sign_tick > 200:

            SEE_WAIVER_VIEW = pygame.transform.scale(SEE_WAIVER_VIEW, (screen_width,screen_height))
            see_rect = SEE_WAIVER_VIEW.get_rect()
            see_rect.center = (screen_width_half, screen_height_half)
            
            scale_img = pygame.transform.smoothscale(img, (screen_width, screen_height))
            rect = scale_img.get_rect()
            rect.center = (screen_width_half, screen_height_half + seq_offset_y)

        else:
            # 부드러운 렌더링
            scale_img = pygame.transform.smoothscale(img, (screen_width, screen_height))
            
            rect = scale_img.get_rect()
            rect.center = (screen_width_half, screen_height_half)
        
        screen.blit(scale_img, rect)

        if img == GAMEROOM_DEALER_FACE_3:
            if sign_tick <= 200:
                talk_text_move("PLEASE SIGN THE WAIVER.")
            elif sign_tick > 202:
                screen.blit(SEE_WAIVER_VIEW, see_rect)
                WAIVER_ON_TABLE_btn.btn_rect = WAIVER_ON_TABLE_btn.image_btn.get_rect(topleft=(WAIVER_ON_TABLE_btn.x_pos, WAIVER_ON_TABLE_btn.y_pos))
                # 버튼 그리기
                WAIVER_ON_TABLE_btn.check_for_hover(mouse_pos)
                WAIVER_ON_TABLE_btn.update(screen) 

talk_text_index = 0
talk_text_timer = 0
talk_text = get_font(80)

def talk_text_move(text):
    global talk_text_index, talk_text_timer, shaking_bool

    # 대사 박스 만들기
    talk_box_w = int(screen_width * 0.5681)
    talk_box_h = int(screen_height * 0.1300)
    talk_box_x = int(screen_width * 0.2153)
    talk_box_y = int(screen_height * 0.7833)
    talk_box = pygame.Surface((talk_box_w, talk_box_h))
    talk_box.fill((0, 0, 0))


    # 글자 띄우기
    full_text_sur = talk_text.render(text, True, (255, 255, 255))
    full_rect = full_text_sur.get_rect()
    box_center_x = talk_box_x + (talk_box_w / 2)
    box_center_y = talk_box_y + (talk_box_h / 2)
    full_rect.center = (box_center_x, box_center_y)

    text_start_x = full_rect.x
    text_start_y = full_rect.y

    if talk_text_index < len(text):
        talk_text_timer += 1
        if talk_text_timer >= 5: 
            talk_text_index += 1
            talk_text_timer = 0

    current_text = text[:talk_text_index]
        
    text_surface = talk_text.render(current_text, True, (255, 255, 255))

    # 진동 효과 만들기
    shaking_bool = True
    shake_offset = shaking_camera(1.9, 0.09, 0.09)
    seq_sway_x= shake_offset[0]
    seq_offset_y= shake_offset[1]

    # 스크린 블릿
    screen.blit(talk_box, (talk_box_x+ seq_sway_x, talk_box_y + seq_offset_y))
    screen.blit(text_surface, (text_start_x + seq_sway_x, text_start_y + seq_offset_y))
    return

up_waiver_tick = 0
dis_img_tick = 0
IMG_x_position = 0
IMG_y_position = 0
img_x = 0
img_y = 0

GAMEROOM_TABLE_IMG = pygame.image.load("sign_imgs/gameroom_table.png").convert_alpha()
gameroom_table_img = pygame.transform.smoothscale(GAMEROOM_TABLE_IMG,(screen_width, screen_height))

scale_img = pygame.transform.scale(SEE_WAIVER_VIEW,(screen_width, screen_height))
WAIVER_ON_HAND_btn_img = pygame.transform.scale(WAIVER_ON_HAND,(int(0.4865*screen_width), int(0.7433*screen_height)))
WAIVER_ON_HAND_btn = Button(WAIVER_ON_HAND_btn_img, screen_width_half, screen_height_half)

def Complete_sign(mouse_pos):
    global screen, up_waiver_tick, dis_img_tick, IMG_y_position, IMG_x_position, img_x, img_y

    rect = scale_img.get_rect()
    rect.center = (screen_width_half, screen_height_half)
    screen.blit(scale_img, rect)
    if up_waiver_tick <= 5:
        WAIVER_ON_TABLE_img = pygame.transform.smoothscale(WAIVER_ON_TABLE, (int(0.13993*screen_width)+up_waiver_tick*200,int(0.18778*screen_height)+up_waiver_tick*200))
        WAIVER_ON_TABLE_img = pygame.transform.rotate(WAIVER_ON_TABLE_img, -3.2*up_waiver_tick)
        screen.blit(WAIVER_ON_TABLE_img, (int(0.44097*screen_width + up_waiver_tick), int(0.19944*screen_height + up_waiver_tick)))
    elif up_waiver_tick <= 10:
        WAIVER_ON_TABLE_img = pygame.transform.smoothscale(WAIVER_ON_HAND,(int(0.13993*screen_width + 5*200),int(0.18778*screen_height+ 5*200)))
        screen.blit(WAIVER_ON_TABLE_img, WAIVER_ON_TABLE_img.get_rect(center = (screen_width_half, screen_height_half)))
    else:
        WAIVER_ON_TABLE_img = pygame.transform.smoothscale(WAIVER_ON_HAND,(int(0.13993*screen_width + 5*200),int(0.18778*screen_height+ 5*200)))
        screen.blit(WAIVER_ON_TABLE_img, WAIVER_ON_TABLE_img.get_rect(center = (screen_width_half, screen_height_half)))
    
        WAIVER_ON_HAND_btn.check_for_hover(mouse_pos)
        WAIVER_ON_HAND_btn.update(screen)

    up_waiver_tick += 1

# 이미지 로드
BLACK_MONITER_IMG = pygame.image.load("moniter_imgs/moniter_black.png").convert_alpha()
moniter_img = pygame.transform.smoothscale(BLACK_MONITER_IMG, (screen_width, screen_height))

moniter_black_changedTable = pygame.image.load("moniter_imgs/moniter_black_changedTable.png").convert_alpha()
moniter_black_changedTable = pygame.transform.smoothscale(moniter_black_changedTable, (screen_width, screen_height))

HEART_IMG = pygame.image.load("moniter_imgs/heart_img.png").convert_alpha()
HEARTBAR_MONITER_IMG = pygame.image.load("moniter_imgs/heartBar_moniter.png").convert_alpha()
HEARTBAR_MONITER_IMG = pygame.transform.scale(HEARTBAR_MONITER_IMG, (screen_width, screen_height))
HEARTBAR_MONITER_FULL_IMG = pygame.image.load("moniter_imgs/heartBar_moniter_full.png").convert_alpha()
HEARTBAR_MONITER_FULL_img = pygame.transform.scale(HEARTBAR_MONITER_FULL_IMG, (screen_width, screen_height))
MONITER_ROUND_IMG = pygame.image.load("moniter_imgs/moniter_round.png").convert_alpha()
round_moniter_img = pygame.transform.smoothscale(MONITER_ROUND_IMG, (screen_width, screen_height))

MONITER_ROUND_1_IMG = pygame.image.load("moniter_imgs/moniter_round_1.png").convert_alpha()
round_moniter_1_img = pygame.transform.smoothscale(MONITER_ROUND_1_IMG, (screen_width, screen_height))
MONITER_ROUND_2_IMG = pygame.image.load("moniter_imgs/moniter_round_2.png").convert_alpha()
round_moniter_2_img = pygame.transform.smoothscale(MONITER_ROUND_2_IMG, (screen_width, screen_height))
MONITER_ROUND_3_IMG = pygame.image.load("moniter_imgs/moniter_round_3.png").convert_alpha()
round_moniter_3_img = pygame.transform.smoothscale(MONITER_ROUND_3_IMG, (screen_width, screen_height))

ROUND_IMG = pygame.image.load("moniter_imgs/round_img.png").convert_alpha()
WINNER_IMG = pygame.image.load("moniter_imgs/winner.png").convert_alpha()
score_tick = 0

def Complete_sign_onClick(mouse_pos):
    global screen,dis_img_tick, IMG_y_position, IMG_x_position, img_x, img_y, up_waiver_tick, state, score_tick
    if IMG_x_position < 0 and IMG_y_position > screen_height:
        state = 'moniter_in'
        moniter_zoomIn(SEE_WAIVER_VIEW,moniter_img,round_moniter_img,round_moniter_1_img)
        return
        
    else:
        rect = scale_img.get_rect()
        rect.center = (screen_width_half, screen_height_half)
        screen.blit(scale_img, rect)
        WAIVER_ON_TABLE_img = pygame.transform.smoothscale(WAIVER_ON_HAND,(int(0.13993*screen_width + 5*200),int(0.18778*screen_height+ 5*200)))
        WAIVER_ON_TABLE_img = pygame.transform.rotate(WAIVER_ON_TABLE_img, 0.5*dis_img_tick)
        img_x = WAIVER_ON_TABLE_img.get_rect().size[0]
        img_y = WAIVER_ON_TABLE_img.get_rect().size[1]
        IMG_x_position = screen_width_half-(img_x/2) - dis_img_tick * 50
        IMG_y_position = screen_height_half-(img_y/2) + dis_img_tick * 60
        screen.blit(WAIVER_ON_TABLE_img, (IMG_x_position, IMG_y_position))
    dis_img_tick += 1

def moniter_zoomIn(zoom_img, current_black_moniter_img, current_moniter_1_img, current_moniter_2_img, twinkle = True):
    global state, screen, score_tick
    score_tick += 1

    if score_tick <= 10:
        zoom_factor = 1.0 + score_tick * 0.03  # 확대 속도를 확 늘림 아래 2줄까지 AI
        width = int(screen_width * zoom_factor)
        height = int(screen_height * zoom_factor)

        scaled_current = pygame.transform.scale(zoom_img, (width, height))
        rect = scaled_current.get_rect()
        rect.center = (screen_width_half - int(score_tick * 0.01736*screen_width), screen_height_half + int(score_tick * 0.00556*screen_height))

        screen.blit(scaled_current, rect)
    elif score_tick <=15:
        rect = current_black_moniter_img.get_rect()
        rect.center = (screen_width_half, screen_height_half)
        screen.blit(current_black_moniter_img, rect)
    elif score_tick <=30:
        rect = current_moniter_1_img.get_rect()
        rect.center = (screen_width_half, screen_height_half)
        screen.blit(current_moniter_1_img, rect)
    if twinkle and score_tick > 30:
        if score_tick<=180:
            if (score_tick % 40) <= 20:
                rect = current_moniter_2_img.get_rect()
                rect.center = (screen_width_half, screen_height_half)
                screen.blit(current_moniter_2_img, rect)
            else:
                rect = current_moniter_1_img.get_rect()
                rect.center = (screen_width_half, screen_height_half)
                screen.blit(current_moniter_1_img, rect)
        else:
            score_tick = 10
            state = 'moniter_out'
            moniter_zoomOut()
            return
    elif twinkle is not True and score_tick > 30:
        if score_tick<=50:
            rect = current_moniter_1_img.get_rect()
            rect.center = (screen_width_half, screen_height_half)
            screen.blit(current_moniter_1_img, rect)
        elif score_tick<=70:
            rect = current_moniter_2_img.get_rect()
            rect.center = (screen_width_half, screen_height_half)
            screen.blit(current_moniter_2_img, rect)
        else:
            score_tick = 10
            global inGame_tick 
            inGame_tick = 0
            state = 'bullet_zoomOut'
            bullet_zoomOut()
            return

def moniter_zoomOut():
    global screen, score_tick, state
    if score_tick <= 10 and score_tick > 0:
        zoom_factor = 1.0 + score_tick * 0.05  # 확대 속도를 확 늘림 아래 2줄까지 AI
        width = int(screen_width * zoom_factor)
        height = int(screen_height * zoom_factor)

        scaled_current = pygame.transform.scale(GAMEROOM_TABLE_IMG, (width, height))
        rect = scaled_current.get_rect()
        rect.center = (screen_width_half - score_tick * 50, screen_height_half + score_tick * 10)

        screen.blit(scaled_current, rect)
    else:
        state = 'box_pre'
        return
    score_tick-=1

BOX_VIEW = pygame.image.load("box_imgs/box_view.png").convert_alpha()
box_view_img = pygame.transform.smoothscale(BOX_VIEW, (screen_width, screen_height))
CLOSE_BOX = pygame.image.load("box_imgs/box_close.png").convert_alpha()
close_box_img = pygame.transform.smoothscale(CLOSE_BOX, (int(screen_width*0.3236), int(screen_height*0.3117)))
closeBox_btn = Button(close_box_img, int(0.3236*screen_width), int(0.3117*screen_height))
OPEN_BOX = pygame.image.load("box_imgs/box_open.png").convert_alpha()
open_box_img = pygame.transform.smoothscale(OPEN_BOX, (int(screen_width*0.3236), int(screen_height*0.3917)))

inGame_tick = 0
def box_pre(mouse_pos):
    global screen, state, inGame_tick, shaking_bool
    if inGame_tick <=5:
        rect = gameroom_table_img.get_rect()
        rect.center = (screen_width_half, screen_height_half)
        screen.blit(gameroom_table_img, rect)
    elif inGame_tick <=15:
        DURATION = 10
        local_timer = inGame_tick - 5
        progress = local_timer / DURATION
        seq_offset_y = screen_height * 0.03  * progress
        rect = gameroom_table_img.get_rect()
        rect.center = (screen_width_half, screen_height_half+seq_offset_y)
        screen.blit(gameroom_table_img, rect)
    else:
        rect = box_view_img.get_rect()
        rect.center = (screen_width_half, screen_height_half)
        screen.blit(box_view_img, rect)
        if inGame_tick <=30:
            rect = close_box_img.get_rect()
            rect.topleft = (int(screen_width*0.3419), int(screen_height*0.5156))
            screen.blit(close_box_img, rect)
        else:
            shaking_bool = True
            shake_offset = shaking_camera(1.9, 0.1, 0.1)
            seq_sway_x= shake_offset[0]
            seq_offset_y= shake_offset[1]

            closeBox_btn.x_pos = int(screen_width*0.3419) +seq_sway_x
            closeBox_btn.y_pos = int(screen_height*0.5156) + +seq_offset_y
            closeBox_btn.btn_rect = closeBox_btn.image_btn.get_rect(topleft=(closeBox_btn.x_pos, closeBox_btn.y_pos))
            # 버튼 그리기
            closeBox_btn.check_for_hover(mouse_pos)
            closeBox_btn.update(screen) 
    inGame_tick+=1

bool_num = 0
open_box_btn = Button(open_box_img, int(screen_width*0.3236), int(screen_height*0.3917))
def box_open(mouse_pos):
    global screen, inGame_tick, bool_num
    rect = box_view_img.get_rect()
    rect.center = (screen_width_half, screen_height_half)
    screen.blit(box_view_img, rect)
    if inGame_tick<=10:
        rect = close_box_img.get_rect()
        rect.topleft = (int(screen_width*0.3419), int(screen_height*0.5156))
        screen.blit(close_box_img, rect)
    elif inGame_tick <=20:
        DURATION = 10
        local_timer = inGame_tick - 10
        progress = local_timer / DURATION
        seq_offset_y = screen_height * 0.01  * progress
        rect = close_box_img.get_rect()
        rect.topleft = (int(screen_width*0.3419), int(screen_height*0.5156)-seq_offset_y)
        screen.blit(close_box_img, rect)
    else:
        open_box_btn.btn_rect = open_box_btn.image_btn.get_rect(topleft=(int(screen_width*0.3419), int(screen_height*0.4356)))
        # 버튼 그리기
        open_box_btn.check_for_hover(mouse_pos)
        open_box_btn.update(screen)
    inGame_tick+=1

# --- 2. 비율 상수 정의 (원근감 적용) ---

# ==================================
# inGame_imgs 디렉토리 내 이미지 파일
# ==================================
AFTER_SAW_IMG = "inGame_imgs/after_saw.png"
AI_FAKE_BULLET_IMG = "inGame_imgs/AIFakebullet.png"
AI_REAL_BULLET_IMG = "inGame_imgs/AIRealbullet.png"
BEFORE_SAW_IMG = "inGame_imgs/before_saw.png"
BULLET_OPEN_VIEW_IMG = pygame.image.load("inGame_imgs/bulletOpenView.png").convert_alpha()
DEALER_SHOT_DEALER_VIEW_IMG = "inGame_imgs/dealer_shot_dealer_view.png"
DEALER_SHOT_ME_VIEW_IMG = "inGame_imgs/dealer_shot_me_view.png"
FAKE_BULLET_OPEN_IMG = "inGame_imgs/Fakebullet_open.png"
IN_GAME_HEARGAGE_IMG = "inGame_imgs/inGame_heargage.png"
ME_SHOT_DEALER_VIEW_IMG = "inGame_imgs/me_shot_dealer_view.png"
ME_SHOT_ME_VIEW_IMG = "inGame_imgs/me_shot_me_view.png"
MY_BULLET_REMOVING_IMG = "inGame_imgs/MybulletRemoving.png"
MY_FAKE_BULLET_IMG = "inGame_imgs/MyFakebullet.png"
MY_HANDCUFFS_IMG = "inGame_imgs/Myhandcuffs.png"
MY_REAL_BULLET_IMG = "inGame_imgs/MyRealbullet.png"
REAL_BULLET_OPEN_IMG = "inGame_imgs/Realbullet_open.png"
SHOT_CHOICE_IMG = "inGame_imgs/shot_choice.png"
SHOT_CHOICE_ME_IMG = "inGame_imgs/shot_choice_me.png"
SHOT_DEALER_CHOICE_IMG = "inGame_imgs/shot_dealer_choice.png"
WAKEUP_LEFT_IMG = "inGame_imgs/wakeup_left.png"
WAKEUP_RIGHT_IMG = "inGame_imgs/wakeup_right.png"
# ==================================
# money_imgs 디렉토리 내 이미지 파일
# ==================================
LEFTCLIP_CLOSE_IMG = "money_imgs/Leftclip_close.png"
LEFTCLIP_OPEN_IMG = "money_imgs/Leftclip_open.png"
MONEY_BAG_CLOSE_IMG = "money_imgs/moneyBag_close.png"
MONEY_BAG_OPEN_IMG = "money_imgs/moneyBag_open.png"
RIGHTCLIP_CLOSE_IMG = "money_imgs/Rightclip_close.png"
RIGHTCLIP_OPEN_IMG = "money_imgs/Rightclip_open.png"
# ==================================
# AIitem_imgs 디렉토리 내 이미지 파일
# ==================================
AI_ADRENALINE_IMG = "AIitem_imgs/AIadrenaline.png"
AI_BEER_IMG = "AIitem_imgs/AIbeer.png"
AI_CIGARETTE_IMG = "AIitem_imgs/AIcigarette.png"
AI_GLASSES_IMG = "AIitem_imgs/AIglasses.png"
AI_HANDCUFFS_IMG = "AIitem_imgs/AIhandcuffs.png"
AI_INVERTER_IMG = "AIitem_imgs/AIinverter.png"
AI_PHONE_IMG = "AIitem_imgs/AIphone.png"
AI_PILL_IMG = "AIitem_imgs/AIpill.png"
AI_SAW_IMG = "AIitem_imgs/AIsaw.png"
# ==================================
# Myitem_imgs 디렉토리 내 이미지 파일
# ==================================
MY_ADRENALINE_IMG = "Myitem_imgs/Myadrenaline.png"
MY_BEER_IMG = "Myitem_imgs/Mybeer.png"
MY_CIGARETTE_IMG = "Myitem_imgs/Mycigarette.png"
MY_GLASSES_IMG = "Myitem_imgs/Myglasses.png"
MY_HANDCUFFS_IMG = "Myitem_imgs/Myhandcuffs.png"
MY_INVERTER_IMG = "Myitem_imgs/Myinverter.png"
MY_PHONE_IMG = "Myitem_imgs/Myphone.png"
MY_PILL_IMG = "Myitem_imgs/Mypill.png"
MY_SAW_IMG = "Myitem_imgs/Mysaw.png"
# ==================================
# AIturn_btn_imgs 디렉토리 내 이미지 파일
# ==================================
AI_BTTM_LEFT_IMG = "AIturn_btn_imgs/AIbttmleft.png"
AI_BTTM_THREE_IMG = "AIturn_btn_imgs/AIbttmthree.png"
AI_BTTM_TWO_IMG = "AIturn_btn_imgs/AIbttmtwo.png"
AI_BTTM_RIGHT_IMG = "AIturn_btn_imgs/AIbttmright.png"
AI_TOP_LEFT_IMG = "AIturn_btn_imgs/AItopleft.png"
AI_TOP_RIGHT_IMG = "AIturn_btn_imgs/AItopright.png"
AI_TOP_THREE_IMG = "AIturn_btn_imgs/AItopthree.png"
AI_TOP_TWO_IMG = "AIturn_btn_imgs/AItoptwo.png"
# ==================================
# dealer_imgs 디렉토리 내 이미지 파일
# ==================================
DEALER_BULLETING_IMG = "dealer_imgs/dealer_bulleting.png"
DEALER_HANDCUFFS_IMG = "dealer_imgs/dealer_handcuffs.png"
DEALER_HURTED_FACE_IMG = "dealer_imgs/dealer_hurted_face.png"
DEALER_NORMAL_FACE_IMG = "dealer_imgs/dealer_nomal_face.png"
DEALER_NORMAL_HAND_IMG = "dealer_imgs/dealer_nomal_hand.png" # 파일명 오타(nomal) 반영
DEALER_RED_EYES_IMG = "dealer_imgs/dealer_redEyes.png"
DEALER_SHOT_DEALER_PUSH_IMG = "dealer_imgs/dealer_shot_dealer_push.png"
DEALER_SHOT_ME_IMG = "dealer_imgs/dealer_shot_me.png"
DEALER_SHOTGUN_IMG = "dealer_imgs/dealer_shotgun.png"
DEALER_SHOTGUN_AFTER_IMG = "dealer_imgs/dealer_shotgun_after.png"
DEALER_SHOTGUN_BEFORE_IMG = "dealer_imgs/dealer_shotgun_before.png"
# ==================================
# Myturen_btn_imgs 디렉토리 내 이미지 파일
# ==================================
MY_BTTM_LEFT_IMG = "Myturn_btn_imgs/Mybttmleft.png"
MY_BTTM_RIGHT_IMG = "Myturn_btn_imgs/Mybttmright.png"
MY_BTTM_THREE_IMG = "Myturn_btn_imgs/Mybttmthree.png"
MY_BTTM_TWO_IMG = "Myturn_btn_imgs/Mybttmtwo.png"
MY_TOP_LEFT_IMG = "Myturn_btn_imgs/Mytopleft.png"
MY_TOP_RIGHT_IMG = "Myturn_btn_imgs/Mytopright.png"
MY_TOP_THREE_IMG = "Myturn_btn_imgs/Mytopthree.png"
MY_TOP_TWO_IMG = "Myturn_btn_imgs/Mytoptwo.png"

class BoxItemSystem:
    def __init__(self):
        
        self.state = "idle"
        
        # --- [추가 1] 저장소 관리 ---
        # 배치가 완료된 아이템들을 저장할 리스트
        # 형식: {'index': 버튼인덱스, 'image': 이미지객체, 'rect': 위치좌표, 'item_name': 아이템이름(옵션)}
        self.filled_slots = [] 
        
        # 이미 사용된 버튼의 인덱스를 저장하는 세트 (빠른 검색용)
        self.occupied_indices = set()
        
        # 페이드 인 변수
        self.fade_image = None
        self.fade_alpha = 0
        self.fade_speed = 20
        self.fade_pos = None
        self.current_img_pos = 0
        
        # 버튼 변수
        self.buttons = []
        self.target_btn_index = -1 # 현재 이동 목표가 된 버튼의 인덱스
        
        # 이동 모션 변수
        self.moving_image = None
        self.move_start_pos = None
        self.move_target_pos = None
        self.move_progress = 0
        self.move_speed = 0.05

    def start_item_sequence(self, item_image, button_data, is_right_side=False):
        """아이템 획득 시퀀스 시작"""
        # 이미 모든 칸이 꽉 찼는지 확인하는 로직이 필요하다면 여기에 추가
        if len(self.filled_slots) >= len(button_data):
            print("인벤토리가 가득 찼습니다!")
            return

        self.state = "item_fade_in"
        self.fade_image = item_image
        self.fade_alpha = 0
        self.current_img_pos = 1 if is_right_side else 0
        
        rect = self.fade_image.get_rect(center=(screen_width_half, screen_height_half))
        if self.current_img_pos:
            self.fade_pos = rect.bottomright
        else:
            self.fade_pos = rect.bottomleft
            
        self.setup_buttons(button_data)
    
    def setup_buttons(self, button_data):
        """버튼 설정 시 인덱스(ID) 부여"""
        self.buttons = []
        # enumerate를 사용하여 인덱스(i)를 같이 가져옵니다.
        for i, (is_top, img, x_ratio, y_ratio, w_ratio, h_ratio) in enumerate(button_data):
            x = int(x_ratio * screen_width)
            y = int(y_ratio * screen_height)
            w = int(w_ratio * screen_width)
            h = int(h_ratio * screen_height)
            img.set_alpha(0)
            
            scaled_img = pygame.transform.scale(img, (w, h))
            
            if is_top:
                rect = scaled_img.get_rect(bottomleft=(x, y))
            else:
                rect = scaled_img.get_rect(bottomright=(x, y))
            
            self.buttons.append({
                'index': i,          # [중요] 버튼 고유 번호
                'image': scaled_img,
                'rect': rect,
                'pos': rect.center,
                'is_top': is_top
            })
    
    def start_item_motion(self, target_pos, btn_index):
        """이동 시작 시 목표 인덱스 저장"""
        self.state = "item_moving"
        self.target_btn_index = btn_index # [중요] 어디로 가는지 저장
        
        self.moving_image = self.fade_image.copy()
        self.moving_image.set_alpha(255)
        
        if self.current_img_pos:
            rect = self.moving_image.get_rect(bottomright=self.fade_pos)
        else:
            rect = self.moving_image.get_rect(bottomleft=self.fade_pos)
        
        self.move_start_pos = rect.center
        self.move_target_pos = target_pos
        self.move_progress = 0

    def check_hover(self, mouse_pos):
        """마우스가 빈 버튼 위에 있으면 커서 변경"""
        
        # 1. 버튼 선택 단계가 아니면 기본 커서로 돌리고 끝냄
        if self.state != "button_select":
            # 다른 곳에서 커서를 제어할 수도 있으니 여기서는 생략하거나 arrow로 초기화
            # mouse_cursor_arrow() 
            return

        is_hovering_any = False

        for btn in self.buttons:
            # [중요] 이미 아이템이 찬 곳은 손가락 커서 안 뜨게 건너뜀
            if btn['index'] in self.occupied_indices:
                continue
            
            # 마우스가 버튼 영역 안에 들어왔는지 확인
            if btn['rect'].collidepoint(mouse_pos):
                is_hovering_any = True
                break
        
        # 2. 하나라도 겹치면 손가락, 아니면 화살표
        if is_hovering_any:
            mouse_cursor_hand()
        else:
            mouse_cursor_arrow()

    def handle_click(self, mouse_pos):
        """클릭 처리: 이미 아이템이 있는 버튼은 무시"""
        if self.state == "button_select":
            for btn in self.buttons:
                # [추가 2] 이미 점유된(occupied) 버튼이면 클릭 무시
                if btn['index'] in self.occupied_indices:
                    continue
                
                if btn['rect'].collidepoint(mouse_pos):
                    # 버튼 위치와 '인덱스'를 넘겨줌
                    self.start_item_motion(btn['pos'], btn['index'])
                    return "item_button_clicked"
        return None
    
    def update(self):
        if self.state == "item_fade_in":
            self.fade_alpha += self.fade_speed
            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.state = "button_select"
        
        elif self.state == "item_moving":
            self.move_progress += self.move_speed
            if self.move_progress >= 1:
                self.move_progress = 1
                
                # [추가 3] 이동 완료 시 데이터 영구 저장
                self.save_item_to_slot()
                
                self.state = "item_complete"
                self.reset_for_next_item()

    def save_item_to_slot(self):
        """이동이 끝난 아이템을 리스트에 저장하고 자리를 차지함"""
        # 최종 위치 계산
        final_rect = self.moving_image.get_rect(center=self.move_target_pos)
        
        # 정보 저장
        saved_data = {
            'index': self.target_btn_index, # 어떤 버튼에 들어갔는지
            'image': self.moving_image,     # 이미지 객체
            'rect': final_rect              # 화면상 위치
        }
        self.filled_slots.append(saved_data)
        
        # 해당 인덱스 '사용 중' 처리
        self.occupied_indices.add(self.target_btn_index)
        
        print(f"아이템 저장 완료: 슬롯 {self.target_btn_index}번")

    def reset_for_next_item(self):
        """다음 턴을 위해 초기화하되, filled_slots는 유지"""
        self.state = "idle"
        self.fade_image = None
        self.moving_image = None
        self.target_btn_index = -1
    
    def get_inventory_data(self):
        """외부에서 현재 아이템 배치 상황을 가져갈 수 있게 함"""
        return self.filled_slots

    def draw(self, surface, box_view_img, open_box_img):
        # 1. 배경 박스
        view_rect = box_view_img.get_rect(center=(screen_width_half, screen_height_half))
        surface.blit(box_view_img, view_rect)
        
        box_img = pygame.transform.scale(open_box_img, (int(screen_width*0.3236), int(screen_height*0.3917)))
        box_rect = box_img.get_rect(topleft=(int(screen_width*0.3419), int(screen_height*0.4356)))
        surface.blit(box_img, box_rect)

        # 2. 빈 버튼(슬롯) 그리기
        if self.state in ["button_select", "item_moving", "item_fade_in", "idle", "item_complete"]: 
            for btn in self.buttons:
                btn['image'].set_alpha(0)
                surface.blit(btn['image'], btn['rect'])
                
                # (선택 사항) 이미 찬 슬롯은 어둡게 표시하거나 X 표시를 하고 싶다면 여기서 btn['index'] in self.occupied_indices 체크

        # 3. [추가 4] 이미 배치 완료된 아이템들 그리기 (계속 유지됨)
        for item in self.filled_slots:
            surface.blit(item['image'], item['rect'])

        # 4. 현재 움직이거나 페이드인 중인 아이템 그리기 (가장 위)
        if self.state in ["item_fade_in", "button_select"]:
            if self.fade_image:
                temp_img = self.fade_image.copy()
                temp_img.set_alpha(int(self.fade_alpha))
                surface.blit(temp_img, self.fade_pos)
        
        elif self.state == "item_moving":
            if self.moving_image and self.move_start_pos and self.move_target_pos:
                t = self.move_progress
                ease_t = t * t * (3 - 2 * t)
                
                current_x = self.move_start_pos[0] + (self.move_target_pos[0] - self.move_start_pos[0]) * ease_t
                current_y = self.move_start_pos[1] + (self.move_target_pos[1] - self.move_start_pos[1]) * ease_t
                
                rect = self.moving_image.get_rect(center=(current_x, current_y))
                surface.blit(self.moving_image, rect)


# ==================== 수정된 box_item 함수 ====================
test_item = None
def box_item(box_system, user, ai, mouse_pos):
    """
    state가 'item'일 때 호출되는 함수
    이미 박스는 열려있는 상태로 진입함
    """
    global screen, box_view_img, open_box_img, myturn_btn_img, state, test_item
    
    if box_system.state == "idle":
        current=user.start_inven()
        if current == "Handcuffs":
            test_item = pygame.image.load(MY_HANDCUFFS_IMG).convert_alpha()
        elif current == "Beer":
            test_item = pygame.image.load(MY_BEER_IMG).convert_alpha()
        elif current == "Magnifying_Glass":
            test_item = pygame.image.load(MY_GLASSES_IMG).convert_alpha()
        elif current == "Cigarette_Pack":
            test_item = pygame.image.load(MY_CIGARETTE_IMG).convert_alpha()
        elif current == "Hand_Saw":
            test_item = pygame.image.load(MY_SAW_IMG).convert_alpha()
        elif current == "Burner_Phone":
            test_item = pygame.image.load(MY_PHONE_IMG).convert_alpha()
        elif current == "Inverter":
            test_item = pygame.image.load(MY_INVERTER_IMG).convert_alpha()
        elif current == "Expired_Medicine":
            test_item = pygame.image.load(MY_PILL_IMG).convert_alpha()
        elif current == "Adrenaline":
            test_item = pygame.image.load(MY_ADRENALINE_IMG).convert_alpha()
        
        if test_item is not None:
            # 크기 변환 및 시퀀스 시작을 조건문 안으로 이동
            test_item = pygame.transform.scale(test_item, (int(screen_width*0.15), int(screen_height*0.15)))
            box_system.start_item_sequence(test_item, myturn_btn_img, is_right_side=False)
    
    box_system.check_hover(mouse_pos)

    # 2. 시스템 업데이트 및 그리기
    box_system.update()
    box_system.draw(screen, box_view_img, open_box_img)

    # 3. 아이템 획득이 완전히 끝났을 때의 처리 (예: 다시 턴제로 돌아가기 등)
    if box_system.state == "item_complete":
        print("아이템 획득 완료")           
        # 여기서 state를 변경하거나 다음 로직을 수행
        # 예: state = 'main_game_loop' 
        # 임시로 idle로 두어 계속 아이템이 나오게 할 수도 있고, 루프를 끊을 수도 있음
        box_system.state = "idle" # 테스트용: 다시 아이템 나오게 하기
    
myturn_btn_img = [
    [1,pygame.image.load(MY_BTTM_LEFT_IMG), 0.0611, 0.6928, 0.2115, 0.3600],
    [0,pygame.image.load(MY_BTTM_RIGHT_IMG), 0.9465, 0.6906, 0.2063, 0.3561],
    [0,pygame.image.load(MY_BTTM_THREE_IMG), 0.8000, 0.6894, 0.1715, 0.3533],
    [1,pygame.image.load(MY_BTTM_TWO_IMG), 0.2087, 0.6922, 0.1753, 0.3589],
    [1,pygame.image.load(MY_TOP_LEFT_IMG),0.1674, 0.3239, 0.1483, 0.2200],
    [0,pygame.image.load(MY_TOP_RIGHT_IMG), 0.8438, 0.3228, 0.1479, 0.2161],
    [0,pygame.image.load(MY_TOP_THREE_IMG),0.7316, 0.3239, 0.1260, 0.2200],
    [1,pygame.image.load(MY_TOP_TWO_IMG), 0.2802, 0.3239, 0.1264, 0.2178],
]

width = 600
height = 700

def bullet_zoomOut():
    global screen, score_tick, state, inGame_tick, width, height
    
    # [수정] 줌아웃 계산을 함수 맨 위로 올려서 에러(UnboundLocalError) 방지
    # 뒤쪽(70 tick 이후)에서 쓸 변수 미리 계산
    zoom_tick = 10 - score_tick # score_tick이 줄어드는 것을 감안하여 계산
    if zoom_tick < 0: zoom_tick = 0
    
    # 1. 하트바 전체 화면 (0~10)
    if inGame_tick <= 10:
        bullet_open_view = pygame.transform.scale(HEARTBAR_MONITER_FULL_img, (screen_width, screen_height))
        rect = bullet_open_view.get_rect()
        rect.center = (screen_width_half, screen_height_half)
        screen.blit(bullet_open_view, rect)

    # 2. 실탄/공포탄 확인 뷰 (10~60)
    elif inGame_tick <= 60:
        tick = inGame_tick - 10
        if tick <= 10 and tick >= 0:
            # [수정] score_tick(고정값) 대신 tick(변하는 값)을 사용하여 부드럽게 줄어들도록 변경
            # tick이 0일 때(시작)는 가장 크고, 10일 때(끝)는 0이 되어야 함
            reverse_tick = 10 - tick 
            
            zoom_factor = 1.0 + reverse_tick * 0.05  # 1.5배 -> 1.0배로 서서히 감소
            width = int(screen_width * zoom_factor)
            height = int(screen_height * zoom_factor)

            scaled_current = pygame.transform.scale(BULLET_OPEN_VIEW_IMG, (width, height))
            rect = scaled_current.get_rect()
            
            # 위치 보정도 reverse_tick을 사용해 부드럽게 원위치로 이동
            rect.center = (screen_width_half - reverse_tick * 50, screen_height_half + reverse_tick * 10)

            screen.blit(scaled_current, rect)
        else:
            # width, height가 아니라 전체 화면으로 보여주는 것이 자연스러움
            bullet_open_view = pygame.transform.scale(BULLET_OPEN_VIEW_IMG, (screen_width, screen_height))
            rect = bullet_open_view.get_rect()
            rect.center = (screen_width_half, screen_height_half)
            screen.blit(bullet_open_view, rect)
            
        # [추가] 여기에 실탄/공포탄 그림을 그리는 로직을 넣으시면 됩니다.
        # 예: screen.blit(REAL_BULLET_IMG, 위치)
        
    # 3. 테이블로 줌 아웃 (60~70)
    elif inGame_tick <= 70:
        # score_tick을 사용하여 줌아웃 (10에서 0으로 줄어듦)
        zoom_factor = 1.0 + score_tick * 0.03
        
        # 안전장치
        if zoom_factor < 1.0: zoom_factor = 1.0
            
        w_out = int(screen_width * zoom_factor)
        h_out = int(screen_height * zoom_factor)

        scaled_current = pygame.transform.scale(GAMEROOM_TABLE_IMG, (w_out, h_out))
        rect = scaled_current.get_rect()
        # 줌인할 때 썼던 좌표 계산과 반대로
        rect.center = (screen_width_half - score_tick * 100, screen_height_half + score_tick * 20)

        screen.blit(scaled_current, rect)
        score_tick -= 1 # 줌아웃을 위해 값을 줄임
        
    # 4. 딜러 턴으로 넘기기
    else:
        state = 'dealer_bulleting'
        dealer_bulleting()
        return
        
    inGame_tick += 1

def bullet_open():
    global screen, state, score_tick, gameroom_table_img
    
    # 1. 줌인 효과 (테이블 이미지 확대)
    score_tick += 1
    
    # 중심점 잡고 확대 (모니터 위치로 줌인되는 느낌)
    target_img = pygame.transform.scale(box_view_img, (screen_width, screen_height))
    rect = target_img.get_rect()
    
    # 화면 중앙보다 약간 위쪽(모니터 쪽)으로 줌인
    rect.center = (screen_width_half, screen_height_half + int(score_tick * 0.02556*screen_height))
    screen.blit(target_img, rect)

    # 2. 일정 시간 후 다음 단계로 전환
    if score_tick >= 10:
        state = 'moniter_zoomIn_bullet'
        score_tick = 0 # 다음 함수를 위해 타이머 초기화
        moniter_zoomIn(gameroom_table_img, moniter_img, HEARTBAR_MONITER_IMG, HEARTBAR_MONITER_FULL_img, False)
        
def dealer_bulleting():
    global screen, state
    base_img = pygame.transform.scale(BULLET_OPEN_VIEW_IMG, (screen_width, screen_height))
    rect = base_img.get_rect()
    rect.center = (screen_width_half, screen_height_half)
    screen.blit(base_img, rect)
    return
def Adrenaline():
    return
def Glasses():
    return
def Beer():
    return
def Pill():
    return
def Saw():
    return
def cigarette():
    return
def Phone():
    return
def inverter():
    return

box_system = None

# --- 메인 게임 루프 ---
def main():
    global state, credits_elements_y_pos, sign_tick, angle, current_tick, img, up_waiver_tick, talk_text_index, talk_text_timer, score_tick, inGame_tick, box_system
    box_system = BoxItemSystem()
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if state == 'credit' or state == 'lobby' or state == 'corridor' or state == 'sign' or state == 'complete_sign' or state == 'box_pre' or state =='box_open' or state == 'dealer_bulleting':
                    """
                    밑은 단축을 위해서 만들어둔 초기화임. 꼭 제출 전에 확인해서 없애달라고 얘기해줘요..
                    """
                    sign_tick = 0
                    img = None
                    current_tick = 0
                    angle = 0
                    up_waiver_tick = 0
                    talk_text_index = 0
                    talk_text_timer = 0
                    state = 'menu'
                elif state == 'menu':
                    state = 'complete_sign'
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                state = 'bullet_open'
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if state == 'menu':
                    if start_btn.check_for_input(mouse_pos):
                        print("시작 버튼 눌림")
                        fade_out()
                        state = 'lobby'
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
                    mouse_cursor_arrow()
                    state = 'lobby_walk'

                elif state == 'corridor' and CORRIDOR_DOOR_btn.check_for_input(mouse_pos):
                    mouse_cursor_arrow()
                    state = 'corridor_walk'

                elif state == 'sign' and WAIVER_ON_TABLE_btn.check_for_input(mouse_pos):
                    mouse_cursor_arrow()
                    state = 'complete_sign'
                elif state == 'complete_sign' and WAIVER_ON_HAND_btn.check_for_input(mouse_pos):
                    mouse_cursor_arrow()
                    state = 'Complete_sign_onClick'
                elif state == 'box_pre' and closeBox_btn.check_for_input(mouse_pos):
                    inGame_tick = 0
                    maxHp=lsj_r.rint(2,4)
                    user=B_def.Action(maxHp)
                    ai=B_def.Action(maxHp)
                    mouse_cursor_arrow()
                    state = 'box_open'
                elif state == 'box_open' and open_box_btn.check_for_input(mouse_pos):
                    mouse_cursor_arrow()
                    state = 'item'
                    inGame_tick = 0
                elif state == 'item':
                    result = box_system.handle_click(mouse_pos)
                    if result == "item_button_clicked":
                        print("아이템 버튼 클릭!")

        screen.fill(BLACK)
        if state == 'menu':
            menu_blit(mouse_pos)
        elif state == 'credit':
            credit_blit()
        elif state == 'lobby':
            gamelobby_blit(mouse_pos)
        elif state == 'corridor':
            flicker_value = corridor_blit(mouse_pos)
        elif state == 'lobby_walk':
            lobby_walk()
        elif state == 'corridor_walk':
            corridor_walk(flicker_value, mouse_pos)
        elif state == 'sign':
            Sign_blit(mouse_pos)
        elif state == 'complete_sign':
            Complete_sign(mouse_pos)
        elif state == 'Complete_sign_onClick':
            Complete_sign_onClick(mouse_pos)
        elif state == 'moniter_in':
            moniter_zoomIn(SEE_WAIVER_VIEW,moniter_img,round_moniter_img,round_moniter_1_img)
        elif state == 'moniter_out':
            moniter_zoomOut()
        elif state == 'box_pre':
            box_pre(mouse_pos)
        elif state == 'box_open':
            box_open(mouse_pos)
        elif state == 'item':
            box_item(box_system, user, ai, mouse_pos)
        elif state == 'bullet_open':
            bullet_open()
        elif state == 'moniter_zoomIn_bullet':
            # [수정] 줌인 될 때 보여줄 이미지 순서: 박스뷰 -> 블랙모니터 -> 하트바 -> 하트바전체
            # 첫 번째 인자에 box_view_img 대신 확대된 느낌을 이어갈 이미지를 넣어야 자연스럽지만,
            # 현재 구조상 box_view_img를 쓰기로 했다면 유지합니다.
            moniter_zoomIn(gameroom_table_img, moniter_black_changedTable, HEARTBAR_MONITER_IMG, HEARTBAR_MONITER_FULL_img, False)
            
        elif state == 'bullet_zoomOut':
            bullet_zoomOut()
            
        elif state == 'dealer_bulleting':
            dealer_bulleting()
        pygame.display.update()
        TIME.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()