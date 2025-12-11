import lsj_r

# 처음 세팅은 main에서

class Action:
    bullet=[]#'live bullet' or '공포탄' 
    aicount=[0,0]

    def __init__(self,hp_max):
        self.hp_max=hp_max
        self.hp=hp_max
        # self.bullet_in= bullet
        self.inven=[0,0,0,0,0,0,0,0]
        self.shotgun_hp=1
        self.turn_bool=[1,0]
        self.phone_bool=[0,0]
        self.inven_list={
        "Handcuffs": self.Handcuffs,
        "Beer":self.Beer,
        "Magnifying_Glass":self.Magnifying_Glass,
        "Cigarette_Pack":self.Cigarette_Pack,
        "Hand_Saw":self.Hand_Saw,
        "Burner_Phone":self.Burner_Phone,
        "Inverter":self.Inverter,
        "Expired_Medicine":self.Expired_Medicine,
        "Adrenaline":self.Adrenaline
    }
    
    def start_inven(self):
        inven_r_list=list(self.inven_list)[::]          
        for i in list(self.inven_list):
            if self.inven.count(i) == 4:
                inven_r_list.remove(i)
        return lsj_r.Choice(inven_r_list)
    
    def inven_in(self,item,inven_index):
        self.inven[inven_index]=item
    
    def start_Shotgun(self,count):
        Action.bullet=[]
        Action.aicount=[0,0]
        live=int(count/2)
        for i in range(live):
            Action.bullet.append("live bullet")
        
        dummy=int(count-live)
        for i in range(dummy): 
            Action.bullet.append("dummy bullet")
        Action.aicount[0]= live
        Action.aicount[1]= dummy

    def Shotgun(self,Shotgun_Bool,target): #각각 live bullet일시 hp다운 시스템 및 총알은 index -1빠지도록
        if Shotgun_Bool==0:
            if self.bullet[-1]=="live bullet":
                self.hp -= self.shotgun_hp
                Action.aicount[0]-=1
            else:
                self.turn_bool[0]=0
                Action.aicount[1]-=1
        else:
            if self.bullet[-1]== "live bullet":
                target.hp -= self.shotgun_hp
                Action.aicount[0]-=1
            else:
                Action.aicount[1]-=1

        if self.shotgun_hp==2:
            self.shotgun_hp=1
            return "톱"+"live bullet" if self.bullet.pop() == "live bullet" else "dummy bullet"
        return "live bullet" if self.bullet.pop() == "live bullet" else "dummy bullet"
    
    # 모든 아이템 함수는 선택한 아이템 목록값을 0으로 변경합니다.
    def Handcuffs(self,inven_index,ad=0): #턴 여부를 확인하는 리스트 [1]값을 1으로 변경합니다.
        self.turn_bool[1]=1
        if ad == 0:
            self.inven[inven_index]=0
        
    def Beer(self,inven_index,ad=0): #탄약 목록에 가장 마지막값를 반환하며 삭제합니다.
        if ad == 0:
            self.inven[inven_index]=0
        beer_count=self.bullet.pop()
        if beer_count =="live bullet":
            Action.aicount[0]-=1
        else:
            Action.aicount[1]-=1
        return beer_count

    def Magnifying_Glass(self,inven_index,ad=0):#탄약 목록의 가장 마지막값을 반환합니다.
        if ad == 0:
            self.inven[inven_index]=0
        return self.bullet[-1]

    def Cigarette_Pack(self,inven_index,ad=0):#hp+1를 합니다.
        if self.hp_max > self.hp:
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
            return "Unfortunately... that\'s it..."
        else:
            r_index=lsj_r.rint(0,len(self.bullet)-2)
            r_num=len(self.bullet)-r_index
            bullet_type= 1 if Action.bullet[r_index] == "live bullet" else 2
            self.phone_bool=[r_index+1, bullet_type]
            return str(r_num)+"th bullet... "+str(self.bullet[r_index])+"..."

    def Inverter(self,inven_index,ad=0):#극성을 전환시켜준다.
        if ad ==0:
            self.inven[inven_index]=0
        if self.bullet[-1]=="live bullet":
            Action.aicount[0]-=1
            Action.aicount[1]+=1
            self.bullet[-1]="dummy bullet"
        else:
            Action.aicount[0]+=1
            Action.aicount[1]-=1
            self.bullet[-1]="live bullet"

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
#Action.aicount=[실탄 수,공포탄 수]
#ing_bullet = 알수없음 0, 실탄 1 공포탄 2
#유저와 ai 객체 명 각각 user, ai
def ai_turn(ai_class,target,ing_bullet=0):
    ret_list=[]
    while 1:
        end_bool=0

        if len(Action.bullet) == ai_class.phone_bool[0]:
            ing_bullet = ai_class.phone_bool[1]
            ai_class.phone_bool= [0,0]
        #1단계 킬각확인
        if (Action.aicount[1]==0 or ing_bullet==1) and (target.hp== 1): #객체를 넣어 바로 상호작용을 하고 미리 데이터 처리를 한후 후 애니메이션을 사용함
            ret_list.append("총1")
            ret_list.append(ai_class.Shotgun(1,target))
            return ret_list
        if (Action.aicount[1]==0 or ing_bullet==1) and (target.hp==2 and "Hand_Saw" in ai_class.inven):
            inven_index=ai_class.inven.index("Hand_Saw")
            ret_list.append("톱"+str(inven_index))
            ret_list.append(ai_class.Hand_Saw(inven_index))
            ret_list.append("총1")
            ret_list.append(ai_class.Shotgun(1,target))
            return ret_list
        
        #2단계 HP올리기
        if ai_class.hp_max > ai_class.hp:
            if "Cigarette_Pack" in ai_class.inven:
                inven_index=ai_class.inven.index("Cigarette_Pack")
                ret_list.append("담"+str(inven_index))
                ret_list.append(ai_class.Cigarette_Pack(inven_index))
                end_bool=1
            elif "Adrenaline" in ai_class.inven and "Cigarette_Pack" in target.inven:
                target_inven_index=target.inven.index("Cigarette_Pack")
                inven_index=ai_class.inven.index("Adrenaline")
                ret_list.append("아담"+str(target_inven_index)+str(inven_index))
                ret_list.append(ai_class.Adrenaline(inven_index,target,target_inven_index))
                end_bool=1
            elif "Expired_Medicine" in ai_class.inven:
                inven_index=ai_class.inven.index("Expired_Medicine")
                ret_list.append("담"+str(inven_index))
                ret_list.append(ai_class.Expired_Medicine(inven_index))
                end_bool=1
            elif "Adrenaline" in ai_class.inven and "Expired_Medicine" in target.inven:
                target_inven_index=target.inven.index("Expired_Medicine")
                inven_index=ai_class.inven.index("Adrenaline")
                ret_list.append("아약"+str(target_inven_index)+str(inven_index))
                ret_list.append(ai_class.Adrenaline(inven_index,target,target_inven_index))
                end_bool=1
                
        #3단계 변수차단
        if ai_class.turn_bool[1]==0:
            if "Handcuffs" in ai_class.inven:
                inven_index=ai_class.inven.index("Handcuffs")
                ret_list.append("수"+str(inven_index))
                ret_list.append(ai_class.Handcuffs(inven_index))
                end_bool=1
            elif "Adrenaline" in ai_class.inven and "Handcuffs" in target.inven:
                target_inven_index=target.inven.index("Handcuffs")
                inven_index=ai_class.inven.index("Adrenaline")
                ret_list.append("아수"+str(target_inven_index)+str(inven_index))
                ret_list.append(ai_class.Adrenaline(inven_index,target,target_inven_index))
                end_bool=1

        #4단계 정보수집 여기에서 정보 수집 사항 제어 변수 추가 해야함.
        if ing_bullet == 0:
            if "Burner_Phone" in ai_class.inven:
                inven_index=ai_class.inven.index("Burner_Phone")
                ret_list.append("대"+str(inven_index))
                ret_list.append(ai_class.Burner_Phone(inven_index))
                end_bool=1
            elif "Adrenaline" in ai_class.inven and "Burner_Phone" in target.inven:
                target_inven_index=target.inven.index("Burner_Phone")
                inven_index=ai_class.inven.index("Adrenaline")
                ret_list.append("아대"+str(target_inven_index)+str(inven_index))
                ret_list.append(ai_class.Adrenaline(inven_index,target,target_inven_index))
                end_bool=1
            elif "Magnifying_Glass" in ai_class.inven:
                inven_index=ai_class.inven.index("Magnifying_Glass")
                ret_list.append("돋"+str(inven_index))
                ing=ai_class.Magnifying_Glass(inven_index)
                if ing == "live bullet":
                    ing_bullet=1
                else:
                    ing_bullet=2
                ret_list.append(ing)
                end_bool=1
            elif "Adrenaline" in ai_class.inven and "Magnifying_Glass" in target.inven:
                target_inven_index=target.inven.index("Magnifying_Glass")
                inven_index=ai_class.inven.index("Adrenaline")
                ret_list.append("아돋"+str(target_inven_index)+str(inven_index))
                ing=ai_class.Adrenaline(inven_index,target,target_inven_index)
                if ing == "live bullet":
                    ing_bullet=1
                else:
                    ing_bullet=2
                ret_list.append(ing)
                end_bool=1

        #5단계 탄 조작
        if ing_bullet == 2:
            if "Inverter" in ai_class.inven:
                inven_index=ai_class.inven.index("Inverter")
                ret_list.append("인"+str(inven_index))
                ret_list.append(ai_class.Inverter(inven_index))
                end_bool=1
                ing_bullet=1
            elif "Beer" in ai_class.inven:
                inven_index=ai_class.inven.index("Beer")
                ret_list.append("맥"+str(inven_index))
                ret_list.append(ai_class.Beer(inven_index))
                end_bool=1
                ing_bullet=0

        #최종 단계!! 확률 싸움
        if ing_bullet != 0 or end_bool==0:
            if ing_bullet == 1:
                ret_list.append("총1")
                ret_list.append(ai_class.Shotgun(1,target))
                return ret_list
            elif ing_bullet == 2:
                ret_list.append("총0")
                ret_list.append(ai_class.Shotgun(0,target))
                ing_bullet=0
            elif Action.aicount[0] > Action.aicount[1]:
                ret_list.append("총1")
                bullet_bool=ai_class.Shotgun(1,target)
                ret_list.append(bullet_bool)
                if bullet_bool=="live bullet":
                    return ret_list
            elif Action.aicount[0] < Action.aicount[1]:
                ret_list.append("총0")
                bullet_bool=ai_class.Shotgun(0,target)
                ret_list.append(bullet_bool)
                if bullet_bool=="live bullet":
                    return ret_list
            else:
                if lsj_r.rint(1,2) ==1:
                    ret_list.append("총1")
                    bullet_bool=ai_class.Shotgun(1,target)
                    ret_list.append(bullet_bool)
                    if bullet_bool=="live bullet":
                        return ret_list
                else:
                    ret_list.append("총0")
                    bullet_bool=ai_class.Shotgun(0,target)
                    ret_list.append(bullet_bool)
                    if bullet_bool=="live bullet":
                        return ret_list
                    else:
                        ing_bullet=0