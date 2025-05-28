from PIL import Image, ImageDraw, ImageFont
from controlFunctions import BYTES_IN_GB
import psutil


#fonts
#djv
djv_10 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
djv_12 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
djvB_10 = ImageFont.truetype("/usr/share/fonts/truetype/DejaVuSansMono-Bold.ttf", 10)


imageTemplate=None



def init(size):
    global imageTemplate
    imageTemplate = Image.new("1",size)
    draw = ImageDraw.Draw(imageTemplate)

    #title card
    draw.rectangle((0,0,30,11),fill=255)
    draw.text((3,0),f"RAM",font=djvB_10,fill=0)

    RAM_TOTAL=round(psutil.virtual_memory().total/ BYTES_IN_GB,2)
    draw.text((40,-1),f"Size : {RAM_TOTAL} GB",font=djv_12,fill=255)

    #virticle line
    draw.line((37,21,37,61),fill=255)
    draw.line((90,21,90,61),fill=255)

    #lables
    draw.text((0,16),f"Usage",font=djvB_10,fill=255)
    draw.text((43,16),f"Percent",font=djvB_10,fill=255)
    draw.text((96,16),f"Avail",font=djvB_10,fill=255)
    draw.text((0,42),f"Cache",font=djvB_10,fill=255)
    draw.text((43,42),f"Buffers",font=djvB_10,fill=255)
    draw.text((96,42),f"Free",font=djvB_10,fill=255)




def update():
    image= imageTemplate.copy()
    draw=ImageDraw.Draw(image)

    ram_info=psutil.virtual_memory()

    #usage
    d_ram_used=round(ram_info.used / BYTES_IN_GB,2)
    draw.text((0,28),f"{d_ram_used} G",font=djv_10,fill=255)


    #percentage
    d_ram_used_percentage=ram_info.percent
    draw.text((43,28),f"{d_ram_used_percentage} %",font=djv_10,fill=255)


    #available
    d_ram_available=round(ram_info.available/BYTES_IN_GB,2)
    draw.text((96,28),f"{d_ram_available} G",font=djv_10,fill=255)

    
    #cache
    d_ram_cache=round(ram_info.cached/BYTES_IN_GB,2)
    draw.text((0,54),f"{d_ram_cache} G",font=djv_10,fill=255)


    #buffers
    d_ram_buffers=round(ram_info.buffers/BYTES_IN_GB,2)
    draw.text((43,54),f"{d_ram_buffers} G",font=djv_10,fill=255)


    #free
    d_ram_free=round(ram_info.free/BYTES_IN_GB,2)
    draw.text((96,54),f"{d_ram_free} G",font=djv_10,fill=255)


    return image