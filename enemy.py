import B_def
import lsj_r

def deal_items(count): #아이템을 count만큼 나눠주는 함수
    global inven, ai_inven  
    inven = []
    ai_inven = []    
    for i in range(count):
        item = B_def.start_inven() 
        inven.append(item)    
    
    for i in range(count):
        item = B_def.start_inven() 
        ai_inven.append(item) 
def shoot():
    if B_def.bullet=="공포탄":
        #자기에게 쏘고 턴 그대로
    elif B_def.bullet=="실탄":
        #플레이어에게 쏘고 턴 넘김
def ai_turn():
    global ai_inven, inven   
    Magnifying_Glass_USED = 0 
    Handcuffs_USED = 0
    Hand_Saw_USED = 0   
    for i in range(len(ai_inven)):
        item_name = ai_inven[i]
        if item_name != 0 and item_name in B_def.inven_list:          
            if item_name == "Magnifying_Glass":
                if Magnifying_Glass_USED >= 1:
                    continue
                Magnifying_Glass_USED += 1
                use_item = B_def.inven_list[item_name]
                use_item(i, ad=1)               
            elif item_name == "Handcuffs":
                if Handcuffs_USED >= 1:
                    continue
                Handcuffs_USED += 1
                use_item = B_def.inven_list[item_name]
                use_item(i, ad=1)               
            elif item_name == "Hand_Saw":
                if Hand_Saw_USED >= 1:
                    continue
                Hand_Saw_USED += 1
                use_item = B_def.inven_list[item_name]
                use_item(i, ad=1)               
            else:
                use_item = B_def.inven_list[item_name]
                use_item(i, ad=1)
        else:
            shoot()









    




