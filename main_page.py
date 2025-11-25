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
# [최적화 1] 배경 이미지는 투명도가 필요 없으므로 convert()를 사용하여 렌더링 속도 향상
GAME_LOBBY_IMG = pygame.image.load("game_lobby_img/GameLobby.png").convert() 



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
shaking_bool = True
shaking_range = 40
# 레미니스케이트 곡선(∞ 모양)을 위한 각도
shake_angle = 0
shake_speed = 0.02  # 회전 속도 (작을수록 느림)

def shaking_camera():
    global shake_angle
    
    if shaking_bool:
        # 레미니스케이트 곡선 (옆으로 누운 8자) 공식
        shake_angle += shake_speed
        sin_t = math.sin(shake_angle)
        cos_t = math.cos(shake_angle)
        denominator = 1 + sin_t * sin_t
        
        x = shaking_range * cos_t / denominator
        y = shaking_range * sin_t * cos_t / denominator
        
        return (int(x*1.2), int(y*1.2))
    else:
        return (0, 0)
    
GAME_LOBBY_IMG_copy = pygame.transform.smoothscale(GAME_LOBBY_IMG, (int(screen_width*1.2),int(screen_height*1.2)))
LOBBY_DOOR_IMG = pygame.image.load("game_lobby_img/lobby_door.png").convert_alpha()

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
    shake_offset = shaking_camera()
    
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
GAME_LOBBY_FEETO_IMG = pygame.image.load("game_lobby_img/gameLobby_feetO.png").convert_alpha()
GAME_LOBBY_FEETX_IMG = pygame.image.load("game_lobby_img/gameLobby_feetx.png").convert_alpha()
GAME_LOBBY_OPENDOOR_IMG = pygame.image.load("game_lobby_img/gameLobby_open_door.png").convert_alpha()
GAME_LOBBY_OPENDOOR_VIEW_IMG = pygame.image.load("game_lobby_img/corridor_gameLobby_view.png").convert_alpha()

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
        elif kick_timer < 10: # 45 + 20프레임
            current_img = GAME_LOBBY_OPENDOOR_IMG
            DURATION = 15
            local_timer = kick_timer - 45
            progress = local_timer / DURATION

            # 문 열릴 때 반동으로 다시 위로 살짝 듬
            seq_offset_y = math.sin(progress * 2 * math.pi) * 100
            seq_sway_x = 0
        # [3단계: 복도 뷰]
        elif kick_timer < 25: # 65 + 60프레임 (여유롭게)
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
CORRIDOR_lightOn_IMG = pygame.image.load("game_lobby_img/corridor_lightOn.png").convert_alpha()
CORRIDOR_lightOn_IMG = pygame.transform.scale(CORRIDOR_lightOn_IMG, (screen_width,screen_height))
CORRIDOR_lightOff_IMG = pygame.image.load("game_lobby_img/corridor_lightOff.png").convert_alpha()
CORRIDOR_lightOff_IMG = pygame.transform.scale(CORRIDOR_lightOff_IMG, (screen_width,screen_height))

#게임 로비 필요한 요소들 정리
CORRIDOR_DOOR_IMG = pygame.image.load("game_lobby_img/corridor_door.png").convert_alpha()
CORRIDOR_DOOR_IMG = pygame.transform.smoothscale(CORRIDOR_DOOR_IMG, (int(0.1430556*screen_width),int(0.2572222*screen_height)))
# 버튼을 전역으로 선언하지 않고, 함수 내에서 생성
CORRIDOR_DOOR_IMG.set_alpha(0)
CORRIDOR_DOOR_btn = Button(CORRIDOR_DOOR_IMG, int(0.1*screen_width), int(0.4675*screen_height))

SEE_GAMEROOM_DOOR_IMG = pygame.image.load("game_lobby_img/see_gameRoom_door.png").convert_alpha()
SEE_GAMEROOM_DOOR_IMG = pygame.transform.scale(SEE_GAMEROOM_DOOR_IMG, (screen_width,screen_height))

ADD_CORRIDOR_IMG = pygame.image.load("game_lobby_img/add_corridor_img.png").convert_alpha()
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

GAMEROOM_FEETO_IMG = pygame.image.load("game_lobby_img/gameroom_feetO.png").convert_alpha()
GAMEROOM_FEETX_IMG = pygame.image.load("game_lobby_img/gameroom_feetX.png").convert_alpha()
GAMEROOM_DOOR_OPEN_IMG = pygame.image.load("game_lobby_img/gameroom_door_open.png").convert_alpha()
GAMEROOM_VIEW_IMG = pygame.image.load("game_lobby_img/gameroom_view.png").convert_alpha()

def corridor_walk(flicker_value):
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
        offset_y = math.sin(corridor_tick) * 60
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
            DURATION = 10
            local_timer = kick_timer - 10
            progress = local_timer / DURATION
            seq_offset_y = math.sin(progress * 2 * math.pi) * -100
            seq_sway_x = math.cos(progress * 2 * math.pi) * 5
        # [2단계: 문 열림]
        elif kick_timer < 30: 
            current_img = GAMEROOM_DOOR_OPEN_IMG
            DURATION = 10
            local_timer = kick_timer - 20
            progress = local_timer / DURATION

            seq_offset_y = math.sin(progress * 2 * math.pi) * 100
            seq_sway_x = 0
        # [3단계: 복도 뷰]
        elif kick_timer < 50: 
            current_img = GAMEROOM_VIEW_IMG
            DURATION = 20
            local_timer = kick_timer - 30
            progress = local_timer / DURATION
            # 기본 꿀렁임
            seq_offset_y = 0
            seq_sway_x = 0
            # [시선 이동 로직]
            look_right_amount = progress
            seq_sway_x -= look_right_amount
        else:
            state = 'menu'
            return
            
        # 이미지 그리기
        if current_img:
            scaled_seq_img = pygame.transform.scale(current_img, (seq_width, seq_height))
            seq_rect = scaled_seq_img.get_rect()
            # 위치 적용
            seq_rect.center = (screen_width_half + seq_sway_x, screen_height_half + seq_offset_y)
    
            screen.blit(scaled_seq_img, seq_rect)



# --- 메인 게임 루프 ---
def main():
    global state, credits_elements_y_pos, shaking_bool, shake_angle, check_num, corridor_tick, corridor_scale
    global walk_angle, kick_timer, walk_drift_x, walk_tick, walk_scale

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
                    mouse_cursor_arrow()
                    state = 'lobby_walk'  # 새로운 상태 정의
                    IS_WALKING = True
                    walk_scale = 1.2
                    walk_tick = 0.0
                    walk_drift_x = 0.0
                    kick_timer = 0
                    walk_angle = 0.0
                elif state == 'corridor' and CORRIDOR_DOOR_btn.check_for_input(mouse_pos):
                    mouse_cursor_arrow()
                    state = 'corridor_walk'
                    corridor_scale = 1.0
                    corridor_tick = 0.0
                    kick_timer = 0 # [수정됨] 여기서 초기화해야 합니다.
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
            corridor_walk(flicker_value)
        pygame.display.update()
        TIME.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()