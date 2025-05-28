from PIL import Image, ImageDraw, ImageFont
from controlFunctions import get_cpu_temp,get_average_cpu_frequency_mhz
import psutil
import os

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
    draw.text((3,0),f"CPU",font=djvB_10,fill=0)

    #Per-core usage divider
    draw.line((103, 3, 103, 61), fill=255)

    #Load average table
    draw.rectangle((0, 44, 98, 52), fill=255)

    draw.line((0, 52, 0, 64), fill=255)
    draw.line((32, 52, 32, 64), fill=255)
    draw.line((65, 52, 65, 64), fill=255)
    draw.line((98, 52, 98, 64), fill=255)


    draw.text((1,16),f"Usage",font=djvB_10,fill=255)
    draw.line((38,16,38,38),fill=255)
    draw.text((43,16),f"Frequency",font=djvB_10,fill=255)

    draw.text((4, 42), "15 m", font=djvB_10, fill=0)
    draw.text((39, 42), "5 m", font=djvB_10, fill=0)
    draw.text((72, 42), "1 m", font=djvB_10, fill=0)

    


def update():
    image= imageTemplate.copy()
    draw=ImageDraw.Draw(image)

    #temperature
    d_cpu_temp=get_cpu_temp()    
    draw.text((45,0),f"{d_cpu_temp}°C",font=djv_12,fill=255)


    #cpu usage %
    d_cpu_usage=psutil.cpu_percent()
    draw.text((1,28),f"{d_cpu_usage}%",font=djv_10,fill=255)
    
    
    #Per-Core Usage
    per_core= psutil.cpu_percent(percpu=True)
    draw.text((106, 2), f"{per_core[0]:.2f}", font=djv_10, fill=255)
    draw.text((106, 18), f"{per_core[1]:.2f}", font=djv_10, fill=255)
    draw.text((106, 34), f"{per_core[2]:.2f}", font=djv_10, fill=255)
    draw.text((106, 50), f"{per_core[3]:.2f}", font=djv_10, fill=255)

    
    #Load Average . processes pending over time
    load1, load5, load15 = os.getloadavg()
    load1=round(load1, 2)
    load5=round(load5, 2)
    load15=round(load15, 2)
    
    draw.text((5, 53),  f"{load15:.2f}", font=djv_10, fill=255)
    draw.text((37, 53), f"{load5:.2f}", font=djv_10, fill=255)
    draw.text((70, 53), f"{load1:.2f}", font=djv_10, fill=255)


    #Cpu frequency
    d_average_freq=get_average_cpu_frequency_mhz()
    draw.text((43,28),f"{d_average_freq} MHz",font=djv_10,fill=255)

    return image


 