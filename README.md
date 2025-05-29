# OLED Stats Display for Raspberry Pi

A lightweight, customizable stats display built in Python using `luma.oled` and `libgpiod v2`. Designed for Raspberry Pi with a 1.3" OLED screen, it shows real-time hardware and network stats — with physical button-based navigation.

---

## ✨ Features

- 📊 System stats: CPU, RAM, RP1 chip, PMIC, NVMe
- 🌐 Network info: IP address, mDNS, and more
- 🖥️ Multiple screens: Home (main and default), Options (hardware selection), Network
- 🔘 Button navigation (click / long press / double click)
- 💤 Idle timeout with screen saver (prevent screen burning)
- 👀 Cool looking screensaver animation [Robo Eyes]. Shoutout to [sofianhw/RoboEyes](https://github.com/sofianhw/RoboEyes) for the screen saver code used and adapted here!
- 🛠️ Configurable via `config.ini`
- 🔄 Systemd service for auto-start
- 👨‍💻 Developer-friendly structure with virtualenv support

---

## Preview
<img src="images/IMG_3149.HEIC" width="300px"><img src="images/IMG_3150.HEIC" width="300px">
<img src="images/IMG_3151.jpg" width="300px"><img src="images/IMG_3153.HEIC" width="300px">

---

## 📦 Dependencies

- Python 3

- [`libgpiod v2`](https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git)  
> ⚠️ This project **requires `libgpiod v2`**, regardless of Raspberry Pi model.
>    
> It's used for precise button event handling (including timeouts for double-click support).
>  
> DONT PANIC!! ⚠️ You can eleminate / skip  this by either changing the code to libgpiod V1 or if you chose some other way to toggle the screen. Trust me its very simple -> [How to change screen toggle function](#How-to-change-screen-toggle)


## Hardware Requirements
- i2c display ( sh1106 or other 1.3 inch oled display) .. please check luma.oled for supported i2c display  
- 26 awg wires , dupont housing and pins  
BELLOW ARE FOR BUTTON CLICK TOGGLE  
- Capasitor (0.1u)  
- Resistor ( 10k ohms )  
- Tactile Button 


## RC Circuit For Button toggle
<img src="images/rc_circuit.png" width="450px">

You could get around with simple button circuit but the signals wont be clean due to button bouncing issue.  
To know about the button bouncing and rc circuit check on https://youtu.be/tI6B6BRKU5k?si=kr0qGCNcuo0YyN5I


## Optimal wiring diagram
<img src="images/pi_5_wiring.png" width="400px"><img src="images/IMG_3152.HEIC" width="300px">

This diagram represent full wiring setup. For Pi 5 can use 5 pin dupont housing for more clean and minimal setup.



# GETTING STARTED

### 🔍 libgpiod V2

CHECK VERSION
```bash
gpiodetect --version
```

Upgrade libgpiod version 2
- visit := https://libgpiod.readthedocs.io/en/latest/
- make sure to select version 2+  (libhpiod)
- install python binging from the package (gpiod)

## For Development
```bash
git clone https://github.com/xxDURGEXxx/Stats-Oled-Raspberry-Pi-5.git

cd Stats-Oled-Raspberry-Pi-5

python3 -m venv enviroment --system-site-packages

source enviroment/bin/activate

pip install -r requirements.txt

cp config/config.ini.example config/config.ini

python main.py
```


## For End Users(System service setup)
```bash
# 1. 📥 Install the Software
sudo git clone https://github.com/xxDURGEXxx/Stats-Oled-Raspberry-Pi-5.git /usr/local/bin/stats_oled  
cd /usr/local/bin/stats_oled  
python3 -m venv enviroment --system-site-packages  
source enviroment/bin/activate
pip install -r requirements.txt
deactivate

# 2. ⚙️ Configure
sudo mkdir -p /etc/stats_oled
sudo cp config/config.ini.example /etc/stats_oled/config.ini
sudo nano /etc/stats_oled/config.ini  (if there is any changes you want to make)

# 3. 🔁 Create systemd Service
sudo cp systemd/oled-stats.service /etc/systemd/system/oled-stats.service
#Make sure this matches your Python path (default):
#   -ExecStart=/usr/local/bin/stats_oled/enviroment/bin/python /usr/local/bin/stats_oled/main.py

# 4.  Enable run on boot and start
sudo systemctl daemon-reexec
sudo systemctl enable oled-stats
sudo systemctl start oled-stats
```



## How to change screen toggle

You can replace the default button-based toggle logic with your own input system — such as keyboard input, web triggers, or GPIO alternatives.

### 🧩 Where to Modify

In `main.py`, find the following:

- The `button_listener()` function  
- The thread that starts it (e.g., `Thread(target=button_listener, ...)`)

### 🔄 Steps to Replace

1. **Disable the default handler**  
   Comment out or remove the following:
   ```python
   def button_listener():
       ...
    botton_listner_thread = threading.Thread(target=button_listener, daemon=True)
    botton_listner_thread.start()
    ```
2. Write your own input function  
   Create a custom function like:
   ```python
   def custom_toggle():
    # Example input logic here
    toggle_user_event(CONSTANTS.SINGLE_CLICK)
   ```

3. Start the new input handler
    ```python 
    customthread=Thread(target=custom_toggle, daemon=True)
    customthread.start()
    ```

Supported Navigation Constants
Use toggle_user_event() with any of the following:
- SINGLE_CLICK → Next screen or option
- LONG_PRESS → Enter/select
- DOUBLE_CLICK → Go back


## 📜 License

MIT License — see `LICENSE` file for details.

## 🤝 Contributions

Issues and PRs are welcome! Help improve the project or share your mods.