from PIL import Image, ImageDraw, ImageFont
from controlFunctions import check_interface_status,get_wireless_quality,WLAN_INTERFACE
from socket import gethostname

djv_10 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
djvB_10 = ImageFont.truetype("/usr/share/fonts/truetype/DejaVuSansMono-Bold.ttf", 10)
djvB_12 = ImageFont.truetype("/usr/share/fonts/truetype/DejaVuSansMono-Bold.ttf", 12)


imageTemplate=None
dot_count=1

icons={
    'router_12':Image.open('./icons/router_12.png'),
    'earth_12':Image.open('./icons/earth_12.png'),
    'signal_blk_12':Image.open('./icons/signal_blk_12.png'),
    'link_blk_12':Image.open('./icons/link_blk_12.png')
}

def init(size):
    global imageTemplate
    imageTemplate = Image.new("1",size)
    draw = ImageDraw.Draw(imageTemplate)

    # arrow drawing for connection
    draw.line((45,6,107,6),fill=255)
    draw.polygon((103,2,107,6,103,6),fill=255)
    draw.polygon((45,6,49,10,49,6),fill=255)

    #const
    draw.text((0,-1),f'{WLAN_INTERFACE}',font=djvB_12,fill=255)
    d_hostname= gethostname()
    draw.text((0,12),f" - {d_hostname}.local",font=djv_10,fill=255)

    #lables
    draw.text((0,25),f"IP",font=djvB_10,fill=255)
    draw.text((0,37),f"SSID",font=djvB_10,fill=255)

    #bottom table
    draw.line((0, 51, 128, 51), fill=255)
    draw.rectangle((0, 52, 14, 63), fill=255)
    imageTemplate.paste(icons["signal_blk_12"], (2, 52))
    draw.rectangle((37, 52, 51, 63), fill=255)
    imageTemplate.paste(icons["link_blk_12"], (39, 52))
    draw.rectangle((75, 52, 103, 63), fill=255)
    draw.text((76, 51), f"Mbps", font=djv_10, fill=0)




def update():
    image= imageTemplate.copy()
    draw=ImageDraw.Draw(image)

    global dot_count
    d_ssid="...."
    d_signal_level='--'
    d_link_quality='--'
    d_data_rate='--'


    con_status,ip_full,igg=check_interface_status()
    
    if con_status == "disconnected":
        draw.text((112,-2),'.'*dot_count,font=djvB_10,fill=255)
        dot_count=(dot_count%3)+1
        ip_full="...."
    
    else:
        temp_icon= 'earth_12' if con_status == "internet" else "router_12"
        
        image.paste(icons[temp_icon],(115,0))

        wireless_quality=get_wireless_quality()
        d_ssid=wireless_quality['ssid']
        d_signal_level=wireless_quality['signal_level']
        d_link_quality=wireless_quality['link_quality']
        d_data_rate=wireless_quality['bit_rate']

    
    draw.text((30,25),f"{ip_full}",font=djv_10,fill=255)
    draw.text((30,37),f"{d_ssid}",font=djv_10,fill=255)

    draw.text((20,52),f"{d_signal_level}",font=djv_10,fill=255)
    draw.text((57,52),f"{d_link_quality}",font=djv_10,fill=255)
    draw.text((107,52),f"{d_data_rate}",font=djv_10,fill=255)


    return image