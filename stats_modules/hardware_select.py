from PIL import Image, ImageDraw, ImageFont
from . import hardware as _hardware
#fonts
#djv


djv_10 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
djv_12 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)


imageTemplate=None
active=False
selector_index=0

GRID=[
{'x1': 0, 'y1': 15, 'x2': 63, 'y2': 31, 'label': 'CPU','module_name':'cpu'},
{'x1': 0, 'y1': 31, 'x2': 63, 'y2': 47, 'label': 'RAM','module_name':'ram'},
{'x1': 0, 'y1': 47, 'x2': 63, 'y2': 63, 'label': 'NVME','module_name':'nvme'},
{'x1': 64, 'y1': 15, 'x2': 127, 'y2': 31, 'label': 'RP1','module_name':'rp1'},
{'x1': 64, 'y1': 31, 'x2': 127, 'y2': 47, 'label': 'PMIC','module_name':'pmic'}
]

GRID_SIZE=len(GRID)

HARDWARE_MODULES= _hardware.hardware_modules
active_module=None

def init(size):
    global imageTemplate
    imageTemplate = Image.new("1",size)
    draw = ImageDraw.Draw(imageTemplate)
    draw.rectangle((0,0,124,12),fill=255)
    draw.text((14,-1),f'Hardware Select',font=djv_12,fill=0)

    for box in GRID:
        draw.text((box["x1"]+15,box["y1"]+3),f'{box["label"]}',font=djv_10,fill=255)
    
    _hardware.init_modules(size)

def getActive():
    return active

def toggleActive():
    global active,selector_index,active_module
    if active:
        active_module=None
        active=False
        selector_index=0
        return
    
    active=True

# change opion or quit form moduel
def action_next():
    global active_module
    if active_module is not None:
        active_module=None
        return
    global selector_index
    selector_index=(selector_index+1)%GRID_SIZE

# enter to moduel or skip to main from moduel
def action_select():
    global active_module
    if active_module is not None:
        toggleActive()
        return
    active_module=HARDWARE_MODULES[GRID[selector_index]["module_name"]]

# go to main or exit moduel
def action_back():
    global active_module
    if active_module is not None:
        active_module=None
        return
    toggleActive()
    

def update():

    #main
    if not active : return imageTemplate

    #moduel
    if active_module is not None : return active_module["update"]()

    #active/selection
    global selector_index
    image= imageTemplate.copy()
    draw=ImageDraw.Draw(image)
    sel_grid= GRID[selector_index]
    draw.rectangle((sel_grid["x1"],sel_grid["y1"],sel_grid["x2"],sel_grid["y2"]),fill=255)
    draw.text((sel_grid["x1"]+15,sel_grid["y1"]+3),f'{sel_grid["label"]}',font=djv_10,fill=0)
    return image


