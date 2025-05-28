from PIL import Image, ImageDraw, ImageFont
import psutil
import datetime
from controlFunctions import get_cpu_temp,get_wireless_quality,check_interface_status

#fonts
#djv

djv_18 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
djv_10 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
djv_12 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
djvB_10 = ImageFont.truetype("/usr/share/fonts/truetype/DejaVuSansMono-Bold.ttf", 10)
djvB_12 = ImageFont.truetype("/usr/share/fonts/truetype/DejaVuSansMono-Bold.ttf", 12)

icons={
    'wifi_10':Image.open('./icons/earth_10.png'),
    'router_10':Image.open('./icons/router_10.png'),
    'link_12':Image.open('./icons/link_12.png'),
    'signal_12':Image.open('./icons/signal_12.png'),
}

imageTemplate=None

def init(size):
    global imageTemplate
    imageTemplate = Image.new("1",size)
    draw = ImageDraw.Draw(imageTemplate)

    #clock section
    draw.line((24, 0, 24, 64), fill=255)
    draw.rectangle((0, 39, 24, 64), fill=255)

    # CPU Usage and Temp
    draw.polygon([(29, 0), (58, 0), (65, 11), (29, 11)], fill=255)
    draw.text((31, 0), "CPU", font=djvB_10, fill=0)
    draw.rectangle((29, 11, 79, 30), outline=255)
    draw.rectangle((79, 11, 127, 30), outline=255)

    # RAM Usage
    draw.polygon([(29, 33), (58, 33), (65, 44), (29, 44)], fill=255)
    draw.text((31, 33), "RAM", font=djvB_10, fill=0)
    draw.rectangle((29, 44, 76, 63), outline=255)


def update():

    image= imageTemplate.copy()
    draw=ImageDraw.Draw(image)

    # Draw Clock
    time_obj=datetime.datetime.now()
    d_day = time_obj.strftime("%d")
    d_month = time_obj.strftime("%b")
    d_hour = time_obj.strftime("%H")
    d_minute = time_obj.strftime("%M")

    draw.text((0, 0), f"{d_hour}", font=djv_18, fill=255)
    draw.text((0, 19), f"{d_minute}", font=djv_18, fill=255)
    draw.text((3,39 ), f"{d_month}", font=djv_10, fill=0)
    draw.text((3, 51), f"{d_day}", font=djv_10, fill=0)


    # CPU Usage and Temp
    cpu_usage = psutil.cpu_percent()
    cpu_temp = get_cpu_temp()

    draw.text((33, 14), f"{cpu_temp}°", font=djvB_12, fill=255)
    draw.text((84, 14), f"{cpu_usage}", font=djvB_12, fill=255)


    # RAM Usage
    ram = psutil.virtual_memory()
    draw.text((33, 47), f"{ram.percent}", font=djvB_12, fill=255)


    #NETWORK STATS
    w_status, full_ip ,last_ip = check_interface_status()
    if w_status == "disconnected":
        draw.text((115,-2),'XX',font=djv_10,fill=255)
        draw.text((82, 47), "--", font=djvB_12, fill=255)
    elif w_status == "no_internet":
        draw.text((69, -2), f"IP {last_ip}", font=djv_10, fill=255)
        image.paste(icons['router_10'],(115,0))
    elif w_status == "internet":
        draw.text((69, -2), f"IP {last_ip}", font=djv_10, fill=255)
        image.paste(icons['wifi_10'],(115,0))
        
    d_link='--'
    d_signal='--'

    if w_status!= "disconnected":
        d_w_q = get_wireless_quality()
        d_link, d_signal = d_w_q['link_quality'] ,d_w_q['signal_level']
    

    image.paste(icons['link_12'],(88,37))
    image.paste(icons['signal_12'],(88,52))
    
    draw.text((105, 36),f"{d_link}",font=djv_12,fill=255)
    draw.text((105, 51),f"{d_signal}",font=djv_12,fill=255)
    return image


