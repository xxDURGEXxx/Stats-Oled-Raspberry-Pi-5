from PIL import Image, ImageDraw, ImageFont
from controlFunctions import BYTES_IN_GB,get_nvme_temp
import psutil


#fonts
#djv

djv_10 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
djvB_10 = ImageFont.truetype("/usr/share/fonts/truetype/DejaVuSansMono-Bold.ttf", 10)


imageTemplate=None

PROG_X1 , PROG_Y1 = 103 , 15
PROG_X2 , PROG_Y2 = 118 , 63
PROG_HEIGHT= PROG_Y2-PROG_Y1-2

def init(size):
    global imageTemplate
    imageTemplate = Image.new("1",size)
    draw = ImageDraw.Draw(imageTemplate)

    #title card
    draw.rectangle((0,0,30,11),fill=255)
    draw.text((3,0),f"NVME",font=djvB_10,fill=0)

    draw.rectangle((PROG_X1,PROG_Y1,PROG_X2,PROG_Y2),outline=255)

    TOTAL_DISK_MEMORY=round(psutil.disk_usage('/').total/ BYTES_IN_GB,2)
    draw.text((35,0),f"{TOTAL_DISK_MEMORY} G",font=djv_10,fill=255)

    draw.text((0,16),f"Temp",font=djvB_10,fill=255)
    draw.text((0,42),f"Swap",font=djvB_10,fill=255)
    draw.text((43,16),f"Used",font=djvB_10,fill=255)
    draw.text((43,42),f"Free",font=djvB_10,fill=255)


def update():
    image= imageTemplate.copy()
    draw=ImageDraw.Draw(image)
    
    d_nvme_temp=get_nvme_temp()
    draw.text((0,28),f"{d_nvme_temp}°",font=djv_10,fill=255)

    swap = psutil.swap_memory()
    d_swap_used=round(swap.used / BYTES_IN_GB,2)
    draw.text((0,54),f"{d_swap_used} G",font=djv_10,fill=255)

    d_disk_usage = psutil.disk_usage('/')

    d_disk_usage_used=round(d_disk_usage.used / BYTES_IN_GB,2)
    draw.text((43,28),f"{d_disk_usage_used} G",font=djv_10,fill=255)

    d_disk_usage_free=round(d_disk_usage.free / BYTES_IN_GB,2)
    draw.text((43,54),f"{d_disk_usage_free} G",font=djv_10,fill=255)

    d_disk_usage_percent=d_disk_usage.percent 
    prog_height= PROG_Y2-(d_disk_usage_percent/100 * PROG_HEIGHT)

    draw.text((94,0),f"{d_disk_usage_percent} %",font=djv_10,fill=255)
    draw.rectangle((PROG_X1,prog_height,PROG_X2,PROG_Y2),fill=255)


    return image