import pygame
import sys
import socketio
import threading

# ---------------------------------------------------------
# 설정 및 초기화
# ---------------------------------------------------------
sio = socketio.Client()

WIDTH, HEIGHT = 1024, 768
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("멀티플레이 게임")

# 색상 및 폰트
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 50, 50)

try:
    FONT = pygame.font.SysFont('malgungothic', 24)
    FONT_BIG = pygame.font.SysFont('malgungothic', 40, bold=True)
except:
    FONT = pygame.font.Font(None, 24)
    FONT_BIG = pygame.font.Font(None, 40)

# 이미지 로드
try:
    bg_image = pygame.image.load('lobby_ui.png').convert_alpha()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
except:
    bg_image = None

# ---------------------------------------------------------
# 상태 변수
# ---------------------------------------------------------
# 현재 화면 상태: 'LOBBY'(메인), 'POPUP_CREATE'(생성창), 'POPUP_JOIN'(참가창), 'IN_ROOM'(입장완료)
current_state = 'LOBBY' 

room_data = {'players': []}
error_message = "" # 에러 메시지 표시용

# 팝업 입력값 관리
input_nickname = ""
input_password = ""
input_focus = 0 # 0: 닉네임칸, 1: 비밀번호칸

# 클릭 영역 정의 (이미지 좌표에 맞춰 수정하세요)
RECT_HOST_AREA = pygame.Rect(140, 620, 105, 20) # 상단 슬롯/테이블 영역
RECT_SEARCH_BTN = pygame.Rect(140, 640, 140, 20)  # "로비 검색" 글자 영역

# ---------------------------------------------------------
# 네트워크 이벤트
# ---------------------------------------------------------
@sio.event
def connect():
    print("서버 연결됨")

@sio.event
def update_room(data):
    global room_data
    room_data = data

@sio.event
def join_success(data):
    """입장 성공 시 호출"""
    global current_state, error_message
    current_state = 'IN_ROOM'
    error_message = ""
    print("방 입장 성공!")

@sio.event
def error_msg(msg):
    """에러 발생 시 호출 (비번 틀림 등)"""
    global error_message
    error_message = msg
    print(f"에러: {msg}")

@sio.event
def game_start(data):
    print("게임 시작!")

# ---------------------------------------------------------
# 그리기 함수
# ---------------------------------------------------------
def draw_main_ui():
    SCREEN.fill(BLACK)
    if bg_image:
        SCREEN.blit(bg_image, (0, 0))

    # [IN_ROOM 상태일 때만 플레이어 목록 표시]
    if current_state == 'IN_ROOM':
        players = room_data.get('players', [])
        for i in range(4):
            y = 165 + (i * 75)
            if i < len(players):
                p = players[i]
                txt = FONT.render(p['nickname'], True, GREEN)
                SCREEN.blit(txt, (140, y + 10))
                if p.get('is_ready'):
                    SCREEN.blit(FONT.render("READY", True, RED), (425, y + 25))
    
    # 상태별 안내 문구 (디버깅용)
    if current_state == 'LOBBY':
        guide = FONT.render("👆 위쪽 테이블을 눌러 방을 생성하거나, 👇 로비 검색을 눌러 참가하세요.", True, WHITE)
        SCREEN.blit(guide, (250, HEIGHT - 50))

def draw_popup(title):
    """입력 팝업창 그리기 (닉네임 + 비번)"""
    # 반투명 배경
    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    s.fill((0, 0, 0, 200))
    SCREEN.blit(s, (0, 0))

    # 팝업 박스
    cx, cy = WIDTH // 2, HEIGHT // 2
    rect = pygame.Rect(cx - 250, cy - 150, 500, 350)
    pygame.draw.rect(SCREEN, BLACK, rect)
    pygame.draw.rect(SCREEN, GREEN, rect, 3)

    # 제목
    t_surf = FONT_BIG.render(title, True, GREEN)
    SCREEN.blit(t_surf, (cx - t_surf.get_width()//2, cy - 120))

    # 에러 메시지
    if error_message:
        e_surf = FONT.render(error_message, True, RED)
        SCREEN.blit(e_surf, (cx - e_surf.get_width()//2, cy + 130))

    # --- 입력칸 1: 닉네임 ---
    color1 = WHITE if input_focus == 0 else GRAY
    lbl1 = FONT.render("닉네임:", True, GREEN)
    SCREEN.blit(lbl1, (rect.x + 50, rect.y + 100))
    
    pygame.draw.rect(SCREEN, GREEN, [rect.x + 160, rect.y + 95, 300, 40], 2)
    txt1 = FONT.render(input_nickname, True, color1)
    SCREEN.blit(txt1, (rect.x + 160, rect.y + 95))

    # --- 입력칸 2: 비밀번호 ---
    color2 = WHITE if input_focus == 1 else GRAY
    lbl2 = FONT.render("비밀번호:", True, GREEN)
    SCREEN.blit(lbl2, (rect.x + 50, rect.y + 170))

    pygame.draw.rect(SCREEN, GREEN, [rect.x + 160, rect.y + 165, 300, 40], 2)
    # 비밀번호 마스킹 (*) 처리
    masked_pw = "*" * len(input_password)
    txt2 = FONT.render(masked_pw, True, color2)
    SCREEN.blit(txt2, (rect.x + 160, rect.y + 165))

    # 안내
    info = FONT.render("[TAB] 이동  |  [ENTER] 완료  |  [ESC] 취소", True, GRAY)
    SCREEN.blit(info, (cx - info.get_width()//2, rect.bottom - 40))

# ---------------------------------------------------------
# 네트워크 요청 함수 (스레드)
# ---------------------------------------------------------
def send_action(action_type, nick, pw):
    try:
        if not sio.connected:
            sio.connect('http://localhost:8080')
        
        data = {'nickname': nick, 'password': pw}
        if action_type == 'create':
            sio.emit('create_room', data)
        else:
            sio.emit('join_room', data)
    except Exception as e:
        print(f"전송 실패: {e}")

# ---------------------------------------------------------
# 메인 루프
# ---------------------------------------------------------
def main():
    global current_state, input_nickname, input_password, input_focus, error_message

    clock = pygame.time.Clock()
    running = True

    while running:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # 1. 팝업이 떠있을 때 (생성 또는 참가 모드)
            if current_state in ['POPUP_CREATE', 'POPUP_JOIN']:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: # 취소
                        current_state = 'LOBBY'
                        error_message = ""
                    
                    elif event.key == pygame.K_TAB: # 입력칸 이동
                        input_focus = 1 - input_focus # 0 <-> 1 전환
                    
                    elif event.key == pygame.K_RETURN: # 제출
                        if input_nickname and input_password:
                            action = 'create' if current_state == 'POPUP_CREATE' else 'join'
                            # 서버로 전송 (스레드 사용)
                            t = threading.Thread(target=send_action, args=(action, input_nickname, input_password))
                            t.start()
                        else:
                            error_message = "닉네임과 비밀번호를 모두 입력하세요."

                    elif event.key == pygame.K_BACKSPACE: # 지우기
                        if input_focus == 0: input_nickname = input_nickname[:-1]
                        else: input_password = input_password[:-1]
                    
                    else: # 글자 입력
                        if input_focus == 0: input_nickname += event.unicode
                        else: input_password += event.unicode

            # 2. 방에 입장했을 때 (대기방)
            elif current_state == 'IN_ROOM':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: sio.emit('toggle_ready')
                    elif event.key == pygame.K_s: sio.emit('start_game')

            # 3. 메인 로비 (아무것도 안 들어간 상태)
            elif current_state == 'LOBBY':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # 상단 테이블 클릭 -> 방 생성 팝업
                    if RECT_HOST_AREA.collidepoint(event.pos):
                        current_state = 'POPUP_CREATE'
                        input_nickname = ""
                        input_password = ""
                        input_focus = 0
                        error_message = ""
                    
                    # 하단 로비 검색 클릭 -> 방 참가 팝업
                    elif RECT_SEARCH_BTN.collidepoint(event.pos):
                        current_state = 'POPUP_JOIN'
                        input_nickname = ""
                        input_password = ""
                        input_focus = 0
                        error_message = ""

        # 그리기
        draw_main_ui()

        if current_state == 'POPUP_CREATE':
            draw_popup("방 생성하기 (HOST)")
        elif current_state == 'POPUP_JOIN':
            draw_popup("방 참가하기 (GUEST)")

        pygame.display.flip()
        clock.tick(60)

    if sio.connected: sio.disconnect()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()