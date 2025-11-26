import B_def
import lsj_r

def deal_items(count):
   
    global inven, ai_inven
    
   
    inven = []
    ai_inven = []
    
    
    for i in range(count):
        item = B_def.start_inven() 
        inven.append(item)    
    
    

    for i in range(count):
        item = B_def.start_inven() 
        ai_inven.append(item) 
    
   
def ai_use_item():
    global ai_inven, inven
    Magnifying_Glass_USED=0 
    Handcuffs_USED=0
    Hand_Saw_USED=0
    item_name=[]
    item_name=list(ai_inven)
    use_item=B_def.inven_list[item_name]
    item_check = list(ai_inven)
    for i in range(len(item_check)):
        item_name = ai_inven[i]
        if item_name != 0 and item_name in B_def.inven_list and Magnifying_Glass_USED < 1 and Handcuffs_USED < 1 and Hand_Saw_USED < 1:
            if item_name == "Magnifying_Glass":
                Magnifying_Glass_USED += 1
                use_item(i, ad=1)
            elif item_name == "Handcuffs":
                Handcuffs_USED += 1             
                use_item(i, ad=1)
            elif item_name == "Hand_Saw":
                Hand_Saw_USED += 1              
                use_item(i, ad=1)
            else:
                use_item(i, ad=1)


            use_item = B_def.inven_list[item_name]
            print(ai_inven)
            use_item(i, ad=1) 
            print(ai_inven)


        



    

deal_items(3)

ai_use_item()









    


