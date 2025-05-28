from PIL import Image, ImageDraw, ImageFont
from controlFunctions import get_rp1_temp

#fonts
#djv

djv_10 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
djvB_10 = ImageFont.truetype("/usr/share/fonts/truetype/DejaVuSansMono-Bold.ttf", 10)


imageTemplate=None


def init(size):
    global imageTemplate
    imageTemplate = Image.new("1",size)
    draw = ImageDraw.Draw(imageTemplate)

    #title card
    draw.rectangle((0,0,30,11),fill=255)
    draw.text((3,0),f"RP1",font=djvB_10,fill=0)
    draw.text((0,16),f"Temp",font=djvB_10,fill=255)


def update():
    image= imageTemplate.copy()
    draw=ImageDraw.Draw(image)

    #temperature
    d_rp1_temp=get_rp1_temp()
    draw.text((0,28),f"{d_rp1_temp}°",font=djv_10,fill=255)

    return image