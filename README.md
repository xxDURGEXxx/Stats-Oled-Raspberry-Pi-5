# OLED Stats Display for Raspberry Pi

A lightweight, customizable stats display built in Python using `luma.oled` and `libgpiod v2`. Designed for Raspberry Pi with a 1.3" OLED screen, it shows real-time hardware and network stats — with physical button-based navigation.

---

## ✨ Features

- 📊 System stats: CPU, RAM, RP1 chip, PMIC, NVMe
- 🌐 Network info: IP address, mDNS, and more
- 🖥️ Multiple screens: Home (main and default), Options (hardware selection), Network
- 🔘 Button navigation (click / long press / double click)
- 💤 Idle timeout with screen saver
- 🛠️ Configurable via `config.ini`
- 🔄 Systemd service for auto-start
- 👨‍💻 Developer-friendly structure with virtualenv support

---

## 📦 Dependencies

- Python 3.7+
ONLY IMPLIES IF YOU ARE USING BUTTON TO NAVIGATE TO OTHER SCREEN . (BUILD IN AND HAVE TO MODIFY IF YOU WANT TO USE OTHER WAY)
IF YOU ARE NOT COMFORTABLE TO UPGRADE, HAVE TO AMMEND THE CODE ON FUNCTION def button_listener(). If you planned to change the function name do ammend the Thread function name also right bellow it.

on user event toogle_user_event should be called by passing prespecified contant
-SINGLE_CLICK  --> switch to next [ screen / options ]
-LONG_PRESS  --> enter into selection page or select options
-DOUBLE_CLICK --> go back

- [`libgpiod v2`](https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git)
> ⚠️ This project **requires `libgpiod v2`**, regardless of Raspberry Pi model.  
> It's used for precise button event handling (including timeouts for double-click support).




![RC circuit wiring](images/rc_circuit.png)




GETTING STARTED

### 🔍 Check libgpiod version
```bash
gpiodetect --version


Upgrade libgpiod version 
- visit := https://libgpiod.readthedocs.io/en/latest/
- make sure to select version 2+


For Development

git clone https://github.com/xxDURGEXxx/Stats-Oled-Raspberry-Pi-5.git
cd Stats-Oled-Raspberry-Pi-5
python3 -m venv enviroment --system-site-packages
source enviroment/bin/activate
pip install -r requirements.txt
cp config/config.ini.example config/config.ini
python main.py



For End Users(System sercice setup)

1. 📥 Install the Software
sudo git clone https://github.com/xxDURGEXxx/Stats-Oled-Raspberry-Pi-5.git /usr/local/bin/stats_oled
cd /usr/local/bin/stats_oled
python3 -m venv enviroment --system-site-packages
source enviroment/bin/activate
pip install -r requirements.txt
deactivate

2. ⚙️ Configure
sudo mkdir -p /etc/stats_oled
sudo cp config/config.ini.example /etc/stats_oled/config.ini
sudo nano /etc/stats_oled/config.ini  (if there is any changes you want to make)

3. 🔁 Create systemd Service
sudo cp systemd/oled-stats.service /etc/systemd/system/oled-stats.service
Make sure this matches your Python path (default):
ExecStart=/usr/local/bin/stats_oled/enviroment/bin/python /usr/local/bin/stats_oled/main.py

4.  Enable run on boot and start
sudo systemctl daemon-reexec
sudo systemctl enable oled-stats
sudo systemctl start oled-stats