import pyautogui   # pyautogui 라이브러리 
import time      # 시간지연을 위한 time 라이브러리

while True:      # 무한반복
   print(pyautogui.position())   # 현재 마우스포인터의 좌표 표시
   time.sleep(0.1)   