import lsj_r

# 처음 세팅해주는 클래스 만들기!!

class Action:
    bullet=[]#'실탄' or '공포탄' 

    def __init__(self,hp_max):
        self.hp_max=hp_max
        self.hp=hp_max
        # self.bullet_in= bullet
        self.inven=[0,0,0,0,0,0,0,0]
        self.shotgun_hp=1
        self.turn_bool=[1,0]
        self.inven_list={
        "Handcuffs": self.Handcuffs,
        "Beer":self.Beer,
        "Magnifying_Glass":self.Magnifying_Glass,
        "Cigarette_Pack":self.Cigarette_Pack,
        "Hand_Saw":self.Hand_Saw,
        "Burner_Phone":self.Burner_Phone,
        "Inverter":self.Inverter,
        "Expired_Medicine":self.Expired_Medicine,
    }
    
    def start_inven(self):
        inven_r_list=list(self.inven_list)[::]          
        for i in list(self.inven_list):
            if self.inven.count(i) == 4:
                inven_r_list.remove(i)
        return lsj_r.Choice(inven_r_list)
    
    def inven_in(self,item,inven_index):
        self.inven[inven_index]=item
    
    def Shotgun(self,Shotgun_Bool,target): #각각 실탄일시 hp다운 시스템 및 총알은 index -1빠지도록
        if Shotgun_Bool==0:
            if self.bullet[-1]=="실탄":
                self.hp -= self.shotgun_hp
            else:
                self.turn_bool[0]=0
        else:
            if self.bullet[-1]== "실탄":
                target.hp -= self.shotgun_hp
            
        self.shotgun_hp=1
        return "실탄" if self.bullet.pop() == "실탄" else "공포탄"
    
    # 모든 아이템 함수는 선택한 아이템 목록값을 0으로 변경합니다.
    def Handcuffs(self,inven_index,ad=0): #턴 여부를 확인하는 리스트 [1]값을 1으로 변경합니다.
        self.turn_bool[1]=1
        if ad == 0:
            self.inven[inven_index]=0
        
    def Beer(self,inven_index,ad=0): #탄약 목록에 가장 마지막값를 반환하며 삭제합니다.
        if ad == 0:
            self.inven[inven_index]=0
        return self.bullet.pop()

    def Magnifying_Glass(self,inven_index,ad=0):#탄약 목록의 가장 마지막값을 반환합니다.
        if ad == 0:
            self.inven[inven_index]=0
        return self.bullet[-1]

    def Cigarette_Pack(self,inven_index,ad=0):#hp+1를 합니다.
        self.hp+=1
        if ad == 0:
            self.inven[inven_index]=0

    def Hand_Saw(self,inven_index,ad=0):#총hp값을 2로 고정합니다.
        self.shotgun_hp=2
        if ad == 0:
            self.inven[inven_index]=0


    def Burner_Phone(self,inven_index,ad=0):#한발 남은 경우 제외 랜덤한 번수의 탄의 번수랑 극성을 알려준다.
        if ad ==0:
            self.inven[inven_index]=0
        if len(self.bullet) == 1:
            return "안타깝게... 됐군..."
        else:
            r_index=lsj_r.rint(0,len(self.bullet)-2)
            r_num=len(self.bullet)-r_index
            return str(r_num)+"번째 탄... "+str(self.bullet[r_index])+"이다..."

    def Inverter(self,inven_index,ad=0):#극성을 전환시켜준다.
        if ad ==0:
            self.inven[inven_index]=0
        if self.bullet[-1]=="실탄":
            self.bullet[-1]="공포탄"
        else:
            self.bullet[-1]="실탄"

    def Expired_Medicine(self,inven_index,ad=0):#각 50%확률로 2칸 올리기 or 한칸 소모
        if 5 < lsj_r.rint(1,10):
            if self.hp+2>=self.hp_max:
                self.hp=self.hp_max
            else:
                self.hp+=2
        else:
            self.hp -=1
        if ad ==0:
            self.inven[inven_index]=0

    def Adrenaline(self,inven_index,target,target_index):#상대  아이템 삭제
        result = None
        inv_name= target.inven[target_index]
        if inv_name in self.inven_list:
            result = self.inven_list[inv_name](target_index,1)
        self.inven[inven_index]=0
        target.inven[target_index]=0
        return result
#메인에서 ai용 카운트하는 변수 만들어서 사용
#ai_count=[실탄 수,공포탄 수]
def ai_turn(ai_class,ai_count,target,ing_bullet=0):
    if (ai_count[1]==0 or ing_bullet==1) and (target.HP== 1 or (target.HP==2 and "Hand_Saw" in ai_class.inven)):
        if "Hand_Saw" in ai_class.inven:
            ai_class.Hand_Saw()
        target.hp=0
        return None
    
    
#탄 유추, 남은 실탄 공포 갯수 카운트