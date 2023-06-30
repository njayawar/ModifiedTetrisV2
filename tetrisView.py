import RPi.GPIO as GPIO
import time
from tkinter import *
from tkinter import ttk
import threading

GPIO.setwarnings(False)
window = Tk()
window.geometry("140x165")
canvas = Canvas(window, width=140, height=165)
canvas.pack()

bounce_pos = 0
w, h = 8, 9

DISPLAY_STATE = [[canvas.create_oval(15*x+1, 15*y+1, 15*x+15, 15*y+15, fill='black') for x in range(w)] for y in range(h)]
DISPLAY_SCORE = canvas.create_text(100, 150, text=0, fill="black", font=('Helvetica 15 bold'))
DISPLAY_GAME_STATE = canvas.create_oval(1, 141, 1+15, 141+15, fill='red')


BOUNCE_POS0 = 17
BOUNCE_POS1 = 27
BOUNCE_POS2 = 22
REQ_POS0 = 5
REQ_POS1 = 6
REQ_POS2 = 13
REQ_POS3 = 19
DATA_POS0 = 18
DATA_POS1 = 23
DATA_POS2 = 24
DATA_POS3 = 25
DATA_POS4 = 12
DATA_POS5 = 16
DATA_POS6 = 20
DATA_POS7 = 21
GAME_RUNNING = 26

def bouncing_update():
    while True:
        bounce_pos = 0b0
        if(GPIO.input(BOUNCE_POS0) == GPIO.HIGH):
            bounce_pos += 1
        if(GPIO.input(BOUNCE_POS1) == GPIO.HIGH):
            bounce_pos += (1 << 1)
        if(GPIO.input(BOUNCE_POS2) == GPIO.HIGH):
            bounce_pos += (1 << 2)
        for i in range(8):
            if(i != bounce_pos):
                canvas.itemconfig(DISPLAY_STATE[0][i], fill='black')
            else:
                canvas.itemconfig(DISPLAY_STATE[0][i], fill='green')
                
        if(GPIO.input(GAME_RUNNING) == GPIO.HIGH):
            canvas.itemconfig(DISPLAY_GAME_STATE, fill='green')
        else:
            canvas.itemconfig(DISPLAY_GAME_STATE, fill='red')

def request_update():
    while True:
        for i in range(9):
            OUTBIT3 = (i & (1 << 3)) >> 3
            OUTBIT2 = (i & (1 << 2)) >> 2
            OUTBIT1 = (i & (1 << 1)) >> 1
            OUTBIT0 = (i & (1 << 0)) >> 0
            GPIO.output(REQ_POS3, OUTBIT3)
            GPIO.output(REQ_POS2, OUTBIT2)
            GPIO.output(REQ_POS1, OUTBIT1)
            GPIO.output(REQ_POS0, OUTBIT0)
            time.sleep(0.001)
            data_read = 0
            if(GPIO.input(DATA_POS0) == GPIO.HIGH):
                data_read += 1
            if(GPIO.input(DATA_POS1) == GPIO.HIGH):
                data_read += (1 << 1)
            if(GPIO.input(DATA_POS2) == GPIO.HIGH):
                data_read += (1 << 2)
            if(GPIO.input(DATA_POS3) == GPIO.HIGH):
                data_read += (1 << 3)
            if(GPIO.input(DATA_POS4) == GPIO.HIGH):
                data_read += (1 << 4)
            if(GPIO.input(DATA_POS5) == GPIO.HIGH):
                data_read += (1 << 5)
            if(GPIO.input(DATA_POS6) == GPIO.HIGH):
                data_read += (1 << 6)
            if(GPIO.input(DATA_POS7) == GPIO.HIGH):
                data_read += (1 << 7)
            if(i == 8):
                canvas.itemconfig(DISPLAY_SCORE, text=data_read)
            else:
                GREEN_POS = (data_read >> 4) & 15
                BLUE_POS = data_read & 15
                for j in range(8):
                    if(GREEN_POS < 9 and (8-j) == GREEN_POS):
                        canvas.itemconfig(DISPLAY_STATE[j+1][i], fill='green')
                    elif(BLUE_POS > 0 and (8-j) <= BLUE_POS):
                        canvas.itemconfig(DISPLAY_STATE[j+1][i], fill='blue')
                    else:
                        canvas.itemconfig(DISPLAY_STATE[j+1][i], fill='black')
                    
        
    
    

GPIO.setmode(GPIO.BCM)
GPIO.setup(BOUNCE_POS0, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BOUNCE_POS1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BOUNCE_POS2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(REQ_POS0, GPIO.OUT)
GPIO.setup(REQ_POS1, GPIO.OUT)
GPIO.setup(REQ_POS2, GPIO.OUT)
GPIO.setup(REQ_POS3, GPIO.OUT)
GPIO.setup(DATA_POS0, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DATA_POS1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DATA_POS2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DATA_POS3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DATA_POS4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DATA_POS5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DATA_POS6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DATA_POS7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(GAME_RUNNING, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


threading.Thread(target=request_update).start()
threading.Thread(target=bouncing_update).start()
window.mainloop()
