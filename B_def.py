import lsj_r
hp=0
ai_hp=0
hp_max=2
bullet=[]#'실탄' or '공포탄'
inven=[]
ai_inven=[]
Shotgun_hp=1
turn_bool=[1,0]

def HP_r():
    global hp,ai_hp
    hp_r=lsj_r.rint(2,4)
    hp=ai_hp=hp_r

def bullet_inven():#총개수 /2가 실탄 개수라는 로직 재해석
    total=lsj_r.rint(2,8)
    for i in range(1,total+1):
        if i & 1:
            bullet.append("공포탄")
        else:
            bullet.append("실탄")
    bullet.sort(reverse=True)
    return None

def bullet_Shuffle():
    lsj_r.Shuffle(bullet)

def start_inven():
    inven_r_list=list(inven_list)[::]
    for i in list(inven_list):
        if inven.count(i) ==4:
            inven_r_list.remove(i)
    return lsj_r.Choice(inven_r_list)

def Shotgun(Shotgun_Bool): #각각 실탄일시 hp다운 시스템 및 총알은 index -1빠지도록
    global hp,ai_hp,Shotgun_hp
    if Shotgun_Bool==0:
        if bullet[-1]=="실탄":
            hp -= Shotgun_hp
        else:
            turn_bool[0]=0

    else:
        if bullet[-1]=="실탄":
            ai_hp -= Shotgun_hp

    Shotgun_hp =1
    return 2 if bullet.pop() == "실탄" else 1

# 모든 아이템 함수는 선택한 아이템 목록값을 0으로 변경합니다.
def Handcuffs(inven_index,ad=0): #턴 여부를 확인하는 리스트 [1]값을 1으로 변경합니다.
    global turn_bool
    turn_bool[1]=1
    if ad ==0:
        inven[inven_index]=0
    if ad ==1:
        ai_inven[inven_index]=0
    
def Beer(inven_index,ad=0): #탄약 목록에 가장 마지막값를 반환하며 삭제합니다.
    if ad ==0:
        inven[inven_index]=0
    if ad ==1:
        ai_inven[inven_index]=0
    return bullet.pop()

def Magnifying_Glass(inven_index,ad=0):#탄약 목록의 가장 마지막값을 반환합니다.
    if ad ==0:
        inven[inven_index]=0
    if ad ==1:
        ai_inven[inven_index]=0
    return bullet[-1]

def Cigarette_Pack(inven_index,ad=0):#글로벌로 hp+1를 합니다.
    global hp
    if ad ==0 or ad ==2:
        hp+=1
        
    if ad ==1 or ad ==3:
        ai_hp+=1
    if ad == 0:
        inven[inven_index]=0
    if ad == 1:
        ai_inven[inven_index]=0

def Hand_Saw(inven_index,ad=0):#총hp값을 2로 고정합니다.
    global Shotgun_hp
    Shotgun_hp=2
    if ad ==0:
        inven[inven_index]=0
    if ad ==1:
        ai_inven[inven_index]=0

def Burner_Phone(inven_index,ad=0):#한발 남은 경우 제외 랜덤한 번수의 탄의 번수랑 극성을 알려준다.
    if ad ==0:
        inven[inven_index]=0
    if ad ==1:
        ai_inven[inven_index]=0
    if len(bullet) == 1:
        return "안타깝게... 됐군..."
    else:
        r_index=lsj_r.rint(0,len(bullet)-2)
        r_num=len(bullet)-r_index
        return str(r_num)+"번째 탄... "+str(bullet[r_index])+"이다..."

def Inverter(inven_index,ad=0):#극성을 전환시켜준다.
    if ad ==0:
        inven[inven_index]=0
    if ad ==1:
        ai_inven[inven_index]=0
    if bullet[-1]=="실탄":
        bullet[-1]="공포탄"
    else:
        bullet[-1]="실탄"

def Expired_Medicine(inven_index,ad=0):#각 50%확률로 2칸 올리기 or 한칸 소모
    global hp,ai_hp,hp_max
    if ad ==0 or ad ==2:
        if 5 < lsj_r.rint(1,10):
            if hp+2>=hp_max:
                hp=hp_max
            else:
                hp+=2
        else:
            hp -=1
        
    if ad ==1 or ad ==3:
        if 5 < lsj_r.rint(1,10):
            if ai_hp+2>=hp_max:
                ai_hp=hp_max
            else:
                ai_hp+=2
        else:
            ai_hp -=1
    if ad ==0:
        inven[inven_index]=0
    elif ad ==1:
        ai_inven[inven_index]=0

def Adrenaline(inven_index,ai_inven_index,ad=0):#상대  아이템 삭제
    result = None
    if ad == 0 or ad == 2:
        inv_name= ai_inven[ai_inven_index]
        if inv_name in inven_list:
            result = inven_list[inv_name](ai_inven_index,2)
        inven[inven_index]=0
        ai_inven[ai_inven_index]=0
        return result
    if ad == 1 or ad ==3:
        inv_name=inven[inven_index]
        if inv_name in inven_list:
            result = inven_list[inv_name](inven_index,3)
        inven[inven_index]=0
        ai_inven[ai_inven_index]=0
        return result


inven_list={
        "Handcuffs": Handcuffs,
        "Beer":Beer,
        "Magnifying_Glass":Magnifying_Glass,
        "Cigarette_Pack":Cigarette_Pack,
        "Hand_Saw":Hand_Saw,
        "Burner_Phone":Burner_Phone,
        "Inverter":Inverter,
        "Expired_Medicine":Expired_Medicine,
    }