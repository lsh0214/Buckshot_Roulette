import os
# no_is=int(list(os.urandom(1))[0])
# os.urandom(1)이란 1바이트만큼의 os 노이즈를 pyte 바이트 형태로 받는다 
# 이 값을 list화 하면 10진수 형태로 된 각각의 바이트 별로 나눠 나타나고 
# 이를 인덱싱으로 집어내면 랜덤 노이즈의 바이트를 10진수의 int형태로 받을 수 잇다.
# 랜덤 숫자 기본 형태 0~255: int

def rint(int_start,int_end):
    int_range=int_end-int_start
    bit_len=int_range.bit_length()
    os_bit=(bit_len +7)// 8
    mask=(1 << bit_len) - 1
    while True:
        val=0
        for i in os.urandom(os_bit):#필요한 만큼 os 노이즈 가져오기
            val=(val * 256)+ i
        bit_mask=val & mask 
        if bit_mask <= int_range:
            return int_start+bit_mask
#시작~끝값 노이즈 값을 정수로 뽑아낼 때
#비트 마스킹+기각 샘플링
#모든 범위로써 만드는 원하는 정수 뽑기

#로직 테스트
List=[]
for i in range(1,300000):
    List.append(rint(1,999999999999999999999))
    if i % 1000 == 0:
        print(List)
# print("")
# print("1의 개수:", List.count(1))
# print("2의 개수:", List.count(2))
# print("3의 개수:", List.count(3))
# print("4의 개수:", List.count(4))
# print("5의 개수:", List.count(5))
# print("6의 개수:", List.count(6))
def Shuffle():
    print("os")

