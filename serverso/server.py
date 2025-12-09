import socketio
import eventlet

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

# 방 데이터 저장소
# 구조: { 'room1': { 'password': '1234', 'players': [], 'game_started': False } }
rooms = {} 
sid_to_room = {}

@sio.event
def connect(sid, environ):
    print(f"클라이언트 접속: {sid}")

# --- [1] 방 생성 (Create) ---
@sio.event
def create_room(sid, data):
    room_id = 'room1' # 테스트를 위해 방 번호 고정
    nickname = data['nickname']
    password = data['password']

    # 이미 방이 존재하고 사람이 있다면 생성 불가 (간단한 로직)
    if room_id in rooms and len(rooms[room_id]['players']) > 0:
        sio.emit('error_msg', '이미 방이 존재합니다. 참가를 이용해주세요.', to=sid)
        return

    sio.enter_room(sid, room_id)
    sid_to_room[sid] = room_id

    # 방 정보 새로 생성 (비밀번호 설정)
    rooms[room_id] = {
        'room_id': room_id,
        'password': password, # 비밀번호 저장
        'players': [{'sid': sid, 'nickname': nickname, 'is_ready': False}],
        'game_started': False
    }
    
    print(f"[방 생성] {nickname}님이 방을 만들었습니다. (비번: {password})")
    sio.emit('join_success', rooms[room_id], to=sid) # 입장 성공 알림
    sio.emit('update_room', rooms[room_id], room=room_id)

# --- [2] 방 참가 (Join) ---
@sio.event
def join_room(sid, data):
    room_id = 'room1'
    nickname = data['nickname']
    password = data['password']

    # 방이 없으면 에러
    if room_id not in rooms:
        sio.emit('error_msg', '생성된 방이 없습니다. 먼저 방을 만들어주세요.', to=sid)
        return

    # 비밀번호 틀리면 에러
    if rooms[room_id]['password'] != password:
        sio.emit('error_msg', '비밀번호가 틀렸습니다!', to=sid)
        return

    # 입장 처리
    sio.enter_room(sid, room_id)
    sid_to_room[sid] = room_id

    new_player = {'sid': sid, 'nickname': nickname, 'is_ready': False}
    rooms[room_id]['players'].append(new_player)

    print(f"[방 참가] {nickname}님이 입장했습니다.")
    sio.emit('join_success', rooms[room_id], to=sid)
    sio.emit('update_room', rooms[room_id], room=room_id)

@sio.event
def toggle_ready(sid):
    room_id = sid_to_room.get(sid)
    if room_id in rooms:
        for p in rooms[room_id]['players']:
            if p['sid'] == sid:
                p['is_ready'] = not p['is_ready']
                break
        sio.emit('update_room', rooms[room_id], room=room_id)

@sio.event
def start_game(sid):
    room_id = sid_to_room.get(sid)
    if room_id in rooms:
        sio.emit('game_start', {'map': 'Forest'}, room=room_id)

@sio.event
def disconnect(sid):
    room_id = sid_to_room.get(sid)
    if room_id in rooms:
        rooms[room_id]['players'] = [p for p in rooms[room_id]['players'] if p['sid'] != sid]
        if not rooms[room_id]['players']:
            del rooms[room_id] # 사람 없으면 방 폭파
        else:
            sio.emit('update_room', rooms[room_id], room=room_id)
    if sid in sid_to_room: del sid_to_room[sid]

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 8080)), app)