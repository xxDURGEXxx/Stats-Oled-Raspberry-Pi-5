from gpiod import LineSettings , request_lines 
from gpiod.line import Bias, Edge, Direction ,Value
from time import time , sleep
import threading
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
import atexit
import signal
import stats_modules 
import sys
from screen_saver_moduel.RoboEyes import screensaver
import configparser
import os

app_conf = configparser.ConfigParser()
config_path = "/etc/stats_oled/config.ini"
if not os.path.exists(config_path):
    config_path = "config/config.ini"  # Fallback for devs
app_conf.read(config_path)


# ================== initialize display ================
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)
device_size=device.size
device.show()
device.contrast(app_conf.getint("general","display_contrast",fallback=100)) 

#===inti display template========
stats_modules.init_modules(device_size)
STAT_MODULES=stats_modules.stats_modules
TOTAL_MODULE=stats_modules.moduel_count

#  ==== Gpios ========
CHIP_PATH = "/dev/gpiochip0"
DISPLAY_TOGGLE_BUTTON = app_conf.getint("gpio_map","display_toggle",fallback=4)  
# DISPLAY_POWER=4

# ====== USER EVENTS =====
ACTION_NEXT="action_next"
ACTION_BACK="action_back"
ACTION_SELECT="action_select"

# ==== TIMEOUTS =======
MAIN_LOOP_INTERVAL = 0.2  # MAIN THREAD CLOCK

STATS_UPDATE_INTERVAL = app_conf.getfloat("timeouts","stats_update_interval",fallback=1) # STATS UPDATE FRAME 
SET_BACK_HOME_TIMER = app_conf.getint("timeouts","set_back_home_timer",fallback=300) # ON IDEL STATS RETURN TO HOME
HOME_IDLE_PERIOD = app_conf.getint("timeouts","home_idle_period",fallback=840) # TIMEOUT TO SWITCH TO SCRENSAVER
SCREEN_SAVER_PERIOD = app_conf.getint("timeouts","screen_saver_period",fallback=180) # TIMEOUT TO TURN OF SCRENSAVER

#======= IGNOOT ( SYSTEM CALCULATED ) =====================================
STATS_UPDATE_COUNTER = STATS_UPDATE_INTERVAL / MAIN_LOOP_INTERVAL


#============== GPIO INITIALIZATION ============
lineInitConfig={
    DISPLAY_TOGGLE_BUTTON: LineSettings(
        bias = Bias.PULL_UP,
        edge_detection = Edge.BOTH
    )
}

lineResetConfig={
    DISPLAY_TOGGLE_BUTTON: LineSettings(
        bias = Bias.DISABLED,
        direction=Direction.INPUT,
    )
}

line_controler=request_lines(
    path=CHIP_PATH,
    consumer='stats_oled',
    config=lineInitConfig
)


#===== init scrensaver ============== 
def screensaverRender(img):
    device.display(img)
screensaver.init(device_size=device_size,render_callback=screensaverRender)

# === Cleanup Function ===
def cleanup():
    global line_controler
    try:
        device.clear()
        device.show()
        device.hide()
    except Exception:
        pass

    try:
        line_controler.reconfigure_lines(lineResetConfig)
        line_controler.release()
        print('released')

    except Exception as e:
        print("Line Reset Failed : ", e)
    

# Register cleanup
atexit.register(cleanup)

def handle_exit(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

# ================================ main ======================================
roling=0
user_event=None
cur_showing_index=0
cur_showing_disp=STAT_MODULES[cur_showing_index]

screen_saver_mode=False
start_screen_saver=False
stop_screen_saver= False
screensaver_quick_exit=False

homeIdleTimer = None
switchToHomeTimer = None

def toggle_user_event(user_ev):
    global screen_saver_mode,user_event ,roling

    user_event=None
    if screen_saver_mode : 
        exitScreensaver(True)
    else : 
        user_event=user_ev
        roling=0

def button_listener():
    last_ev_time=0
    LISTERNER_TIMEOUT=10
    DOUBLE_CLICK_TIMEOUT=0.15
    LONG_PRESS_TIMEOUT=0.3

    edge_timeout=LISTERNER_TIMEOUT

    last_ev ="RISING_EDGE"

    while True:
        if line_controler.wait_edge_events(edge_timeout):
            now=time()*1000
            edge=line_controler.read_edge_events()[0].event_type.name
            
            if now-last_ev_time <= 50 or last_ev == edge : continue  # DEBOUNCE

            last_ev_time =now
            last_ev = edge
            if edge == "FALLING_EDGE" :
                if edge_timeout == LISTERNER_TIMEOUT : edge_timeout=LONG_PRESS_TIMEOUT
                if edge_timeout == DOUBLE_CLICK_TIMEOUT : 
                    edge_timeout=LISTERNER_TIMEOUT
                    # DOUBLE CLICK
                    toggle_user_event(ACTION_BACK)

            elif edge == "RISING_EDGE" :
                if edge_timeout == LONG_PRESS_TIMEOUT : edge_timeout = DOUBLE_CLICK_TIMEOUT

        else:
            # LONG PRESS
            if edge_timeout == LONG_PRESS_TIMEOUT : toggle_user_event(ACTION_SELECT)
            # SINGLE CLICK
            elif edge_timeout == DOUBLE_CLICK_TIMEOUT : toggle_user_event(ACTION_NEXT)

            edge_timeout = LISTERNER_TIMEOUT

button_listener_thread = threading.Thread(target=button_listener, daemon=True)

# def user_input_listener() :
#     print('\n')
#     print('OPTIONS AVAILABLE :  next  back  select')
#     while True:
#         act=input("-> ")

#         if act == 'next' : toggle_user_event(ACTION_NEXT)
#         elif act == 'back' : toggle_user_event(ACTION_BACK)
#         elif act == 'select' : toggle_user_event(ACTION_SELECT)
#         else : print("Invalid Input")

# user_input_listener_thread = threading.Thread(target=user_input_listener, daemon=True)

def switchToScreensaver() :
    global screen_saver_mode,switchToHomeTimer,start_screen_saver,stop_screen_saver,screensaver_quick_exit

    screen_saver_mode=True
    start_screen_saver=True
    stop_screen_saver = False
    screensaver_quick_exit=False
    if switchToHomeTimer.is_alive() : switchToHomeTimer.cancel()
    switchToHomeTimer=threading.Timer(SCREEN_SAVER_PERIOD,exitScreensaver)
    switchToHome.daemon =True
    switchToHomeTimer.start()

homeIdleTimer = threading.Timer(HOME_IDLE_PERIOD,switchToScreensaver)
homeIdleTimer.daemon = True
def exitScreensaver(quit_now=False):
    global stop_screen_saver,screensaver_quick_exit

    screensaver_quick_exit=quit_now
    stop_screen_saver=True

def switchToHome() :
    global cur_showing_disp,cur_showing_index,roling,screen_saver_mode,homeIdleTimer

    if switchToHomeTimer.is_alive() : switchToHomeTimer.cancel()
    if homeIdleTimer.is_alive() : homeIdleTimer.cancel()
    cur_showing_index=0
    cur_showing_disp=STAT_MODULES[cur_showing_index]
    screen_saver_mode=False
    roling=0
    homeIdleTimer = threading.Timer(HOME_IDLE_PERIOD,switchToScreensaver)
    homeIdleTimer.daemon = True
    homeIdleTimer.start()

switchToHomeTimer = threading.Timer(SET_BACK_HOME_TIMER,switchToHome)
switchToHomeTimer.daemon = True

def screenUpdater():
    global cur_showing_index,cur_showing_disp,switchToHomeTimer,homeIdleTimer
    if user_event is not None:
        if not cur_showing_disp.get("active") or not cur_showing_disp["active"]():
            if(user_event==ACTION_NEXT):
                cur_showing_index=(cur_showing_index+1) % TOTAL_MODULE
                cur_showing_disp = STAT_MODULES[cur_showing_index]
            elif(user_event==ACTION_BACK):
                cur_showing_index=(cur_showing_index-1) % TOTAL_MODULE
                cur_showing_disp = STAT_MODULES[cur_showing_index]
            elif(user_event==ACTION_SELECT):
                if cur_showing_disp.get("toggleActive") : cur_showing_disp["toggleActive"]()
                else : return False
        else:
            cur_showing_disp[user_event]()

        #===== Run setTimeouts according to display on button intrupt ==========
        if  switchToHomeTimer.is_alive() : switchToHomeTimer.cancel()
        
        if homeIdleTimer.is_alive() : homeIdleTimer.cancel()
            
        if cur_showing_index == 0:
            homeIdleTimer = threading.Timer(HOME_IDLE_PERIOD,switchToScreensaver)
            homeIdleTimer.daemon = True
            homeIdleTimer.start()
        else : 
            switchToHomeTimer=threading.Timer(SET_BACK_HOME_TIMER,switchToHome)
            switchToHomeTimer.daemon = True
            switchToHomeTimer.start()

    device.display( cur_showing_disp["update"]() )
    return True

#===========run before start================

homeIdleTimer.start()
button_listener_thread.start()
# user_input_listener_thread.start()



#====== main loop =========
while True :
    if screen_saver_mode:
        if start_screen_saver : 
            device.clear()
            device.show()
            screensaver.start()
            start_screen_saver= False
        
        if stop_screen_saver : 
            screensaver.stop(screensaver_quick_exit)
            stop_screen_saver=False
        
        if not screensaver.is_active:
            device.clear()
            device.show()
            switchToHome()

    else :
        if roling==0 :
            if screenUpdater() :
                roling=STATS_UPDATE_COUNTER
            user_event= None

        roling-=1
        
    sleep(MAIN_LOOP_INTERVAL)  
    

