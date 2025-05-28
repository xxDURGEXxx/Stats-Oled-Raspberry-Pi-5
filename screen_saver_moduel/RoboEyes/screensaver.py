import pygame
from .RoboEyes import RoboEyes,Mood,Position,BGCOLOR,MAINCOLOR
from PIL import Image,ImageDraw
import threading
from time import sleep
import random

SCREEN_WIDTH=None
SCREEN_HEIGHT=None

canvas = None
robo_eyes=None
output_callback=None
clock = pygame.time.Clock()

storyEv=threading.Event()
closingEv=threading.Event()

storyThread = None
updatorThread= None
closingThread = None

continue_story=False

storyCollection=[]
AVAILABLE_STORY=0

is_active=False

def init(device_size,render_callback):
    global canvas,robo_eyes,output_callback,clock,SCREEN_HEIGHT,SCREEN_WIDTH

    SCREEN_WIDTH,SCREEN_HEIGHT=device_size
    output_callback=render_callback

    canvas = pygame.Surface(device_size)
    canvas.fill(BGCOLOR)

    robo_eyes = RoboEyes(canvas,width=SCREEN_WIDTH,height=SCREEN_HEIGHT,frame_rate=20)
    robo_eyes.setAutoblinker(True,interval=2,variation=3)
    robo_eyes.setIdleMode(False,interval=1,variation=3)

def updator(ev) :
    #buffoer for animmation  start
    sleep(0.1)
    while ev.is_set():
        robo_eyes.update()
        raw_str = pygame.image.tostring(canvas, "RGB")
        img = Image.frombytes("RGB", (SCREEN_WIDTH, SCREEN_HEIGHT), raw_str).convert("1") 
        output_callback(img)
        clock.tick(30)


def start() :
    global updatorThread,storyThread,continue_story,is_active
    resetRobotState()
    robo_eyes.update()
    if storyEv.is_set() : storyEv.clear()
    if closingThread.is_alive() : closingEv.clear()
    continue_story=True
    storyEv.set() 
    updatorThread=threading.Thread(target=updator,daemon=True,args=(storyEv,))
    updatorThread.start()
    storyThread=threading.Thread(target=story_runner, daemon=True,args=(storyEv,))
    storyThread.start()
    is_active=True

def trackStoryClosing(ev):
    global storyThread
    while storyThread.is_alive() and ev.is_set():
        sleep(0.1)
    
    if ev.is_set() : cleanExit()

def stop(instant=False):
    global continue_story,closingThread
    if instant : 
        cleanExit()
        return
    
    continue_story=False
    if closingThread.is_alive() : closingEv.clear()
    closingEv.set()
    closingThread=threading.Thread(target=trackStoryClosing, daemon=True,args=(closingEv,))
    closingThread.start()

def cleanExit():
    global is_active
    closingEv.clear()
    storyEv.clear()
    sleep(0.1)
    is_active=False

    

def wait_with_check(duration):
    if duration<0.1 :
        sleep(duration)
        if not storyEv.is_set() : return False
    else :
        for _ in range(int(duration * 10)):
            if not storyEv.is_set() : return False
            sleep(0.1)
    return True

def story_runner(ev):

    if not openingAnimation() : return

    while continue_story:
        story_selector=random.randint(0,AVAILABLE_STORY-1)
        # story_selector=1
        resetRobotState()
        if not wait_with_check(2): return
        if not storyCollection[story_selector]() : return
    
    if not closingAnimation() : return


def openingAnimation():
    robo_eyes.eyeLy=(robo_eyes.eyeLheight_default*-1)-10
    robo_eyes.eyeRy=robo_eyes.eyeLy
    robo_eyes.eyeLy_next=robo_eyes.eyeLy
    robo_eyes.eyeRy_next=robo_eyes.eyeRy
    robo_eyes.autoblinker=False
    while robo_eyes.eyeLy_next < robo_eyes.eyeLy_default:
        robo_eyes.eyeLy_next+=1
        if not wait_with_check(0.05) : return
    robo_eyes.setPosition()
    robo_eyes.autoblinker=True
    return True

def closingAnimation():
    robo_eyes.autoblinker=False
    while not robo_eyes.eyeLy > SCREEN_HEIGHT:
        robo_eyes.eyeLy_next+=1
        if not wait_with_check(0.05) : return
    if not wait_with_check(0.5) : return


def resetRobotState():
    robo_eyes.setPosition()
    robo_eyes.setAutoblinker(True,interval=2,variation=3)
    robo_eyes.setIdleMode(False,interval=1,variation=3)
    robo_eyes.setMood(Mood.DEFAULT)
    robo_eyes.setCuriosity(False)
    robo_eyes.setHFlicker(False)
    robo_eyes.setVFlicker(False)
    robo_eyes.eyes_same_y=True
    robo_eyes.setHeight()


#====== search and angry ========
def story1():
    robo_eyes.setCuriosity(True)
    if not wait_with_check(3): return

    robo_eyes.idle=True
    if not wait_with_check(10): return

    robo_eyes.idle=False
    robo_eyes.setPosition()
    if not wait_with_check(1) : return

    robo_eyes.setMood(Mood.ANGRY)
    if not wait_with_check(2): return 
    
    robo_eyes.setPosition(Position.E)
    if not wait_with_check(3) : return

    robo_eyes.setPosition(Position.W)
    if not wait_with_check(3) : return

    robo_eyes.setPosition(Position.E)
    if not wait_with_check(3) : return

    robo_eyes.setPosition()
    if not wait_with_check(3) : return

    robo_eyes.setMood(Mood.DEFAULT)
    robo_eyes.setCuriosity(False)

    return True

storyCollection.append(story1)

#======= Happy and playfull========
def story2():
    robo_eyes.setMood(Mood.HAPPY)
    if not wait_with_check(3): return

    robo_eyes.setMood(Mood.DEFAULT)
    if not wait_with_check(1): return

    robo_eyes.autoblinker=False
    if not wait_with_check(1) : return

    for i in range(1,22):
        robo_eyes.eyeLx_next-=2
        robo_eyes.eyeRx_next+=2
        robo_eyes.space_between_next+=4
        sleep(0.01)
    
    if not wait_with_check(1.5): return

    for i in range(1,22):
        robo_eyes.eyeLx_next+=2
        robo_eyes.eyeRx_next-=2
        robo_eyes.space_between_next-=4
        sleep(0.01)
    if not wait_with_check(1): return

    robo_eyes.close(left=False)
    if not wait_with_check(0.8): return

    robo_eyes.open_eyes(left=False)
    if not wait_with_check(1): return

    robo_eyes.autoblinker=True
    robo_eyes.anim_laugh()
    if not wait_with_check(2): return

    robo_eyes.setCuriosity(True)
    robo_eyes.idle=True
    if not wait_with_check(10): return
    
    robo_eyes.setCuriosity(False)
    robo_eyes.idle=False
    robo_eyes.setPosition()
    if not wait_with_check(2): return

    robo_eyes.autoblinker=False
    if not wait_with_check(1) : return
    robo_eyes.eyes_same_y=False
    for i in range(1,26):
        robo_eyes.eyeLx_next-=1
        robo_eyes.eyeRx_next+=2
        robo_eyes.eyeLy_next-=1
        robo_eyes.eyeRy_next+=2
        robo_eyes.space_between_next+=3
        if not wait_with_check(0.05): return
    
    if not wait_with_check(1): return

    for i in range(1,26):
        robo_eyes.eyeLx_next+=1
        robo_eyes.eyeRx_next-=2
        if robo_eyes.eyeLheight_default+robo_eyes.eyeLy+2<SCREEN_HEIGHT : robo_eyes.eyeLy_next+=2  
        if robo_eyes.eyeRy-3 >0 : robo_eyes.eyeRy_next-=3
        robo_eyes.space_between_next-=3
        if not wait_with_check(0.05): return
    if not wait_with_check(0.4): return

    robo_eyes.setMood(Mood.TIRED)
    if not wait_with_check(1): return

    robo_eyes.anim_confused()
    if not wait_with_check(0.5) : return
    robo_eyes.eyes_same_y=True
    robo_eyes.setPosition()
    if not wait_with_check(0.5) : return
                
    robo_eyes.autoblinker=True
    robo_eyes.setMood(Mood.DEFAULT)
    if not wait_with_check(1) : return      

    robo_eyes.setMood(Mood.HAPPY)
    if not wait_with_check(3) : return   

    robo_eyes.setMood(Mood.DEFAULT)

    return True
storyCollection.append(story2)

#======= Tired and sleepy========
def story3():
    robo_eyes.idle=True
    if not wait_with_check(10): return

    robo_eyes.idle=False
    robo_eyes.setPosition()
    if not wait_with_check(2): return

    robo_eyes.setMood(Mood.TIRED)
    if not wait_with_check(4): return

    robo_eyes.autoblinker=False
    if not wait_with_check(1.5) : return

    eye_sleepy_close= robo_eyes.eyeLheight_default
    close_speed=1.5
    while eye_sleepy_close>10:
        eye_sleepy_close-=5
        robo_eyes.close()
        if not wait_with_check(0.5) : return
        robo_eyes.setHeight(eye_sleepy_close,eye_sleepy_close)
        if not wait_with_check(close_speed) : return
        robo_eyes.open_eyes()
        robo_eyes.eyeLy_next += 2
        robo_eyes.eyeRy_next += 2
        close_speed+=0.1

    robo_eyes.setHeight(5,5)
    if not wait_with_check(0.5) : return

    while robo_eyes.eyeLy_next < SCREEN_HEIGHT-5 :
        robo_eyes.eyeLy_next += 1
        robo_eyes.eyeRy_next += 1
        if not wait_with_check(0.05) : return
    

    robo_eyes.setMood(Mood.DEFAULT)
    robo_eyes.open_eyes()
    robo_eyes.setHeight()
    robo_eyes.setPosition()

    robo_eyes.blink()
    if not wait_with_check(0.3) : return

    robo_eyes.blink()
    if not wait_with_check(0.3) : return

    robo_eyes.blink()
    if not wait_with_check(0.5) : return

    robo_eyes.blink()
    if not wait_with_check(0.1) : return

    robo_eyes.setHFlicker(True,10)
    if not wait_with_check(2) : return

    robo_eyes.setHFlicker(False,10)

    robo_eyes.autoblinker=True
    if not wait_with_check(3) : return

    robo_eyes.setMood(Mood.TIRED)
    if not wait_with_check(2) : return

    eye_sleepy_close= robo_eyes.eyeLheight_default
    for i in range(1,5) :
        eye_sleepy_close-=4
        robo_eyes.setHeight(eye_sleepy_close,eye_sleepy_close)
        if not wait_with_check(0.2) : return
    if not wait_with_check(2) : return

    robo_eyes.setMood(Mood.DEFAULT)
    robo_eyes.setHeight()
    robo_eyes.setHFlicker(True,10)
    if not wait_with_check(1.5) : return

    robo_eyes.setHFlicker(False,10)
    if not wait_with_check(4) : return

    return True
storyCollection.append(story3)

storyThread=threading.Thread(target=story_runner, daemon=True,args=(storyEv,))
updatorThread=threading.Thread(target=updator, daemon=True,args=(storyEv,))
closingThread=threading.Thread(target=trackStoryClosing, daemon=True,args=(closingEv,))
AVAILABLE_STORY=len(storyCollection)