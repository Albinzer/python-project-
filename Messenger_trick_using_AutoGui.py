import pyautogui
import time

message=3
while message > 0:
    time.sleep(5)
    pyautogui.typewrite('Hello , Do you wanna something ')
    time.sleep(2)
    pyautogui.press('enter')
    message -= 1




