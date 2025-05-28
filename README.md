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
- [`libgpiod v2`](https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git)

> ⚠️ This project **requires `libgpiod v2`**, regardless of Raspberry Pi model.  
> It's used for precise button event handling (including timeouts for double-click support).




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

sudo git clone https://github.com/xxDURGEXxx/Stats-Oled-Raspberry-Pi-5.git /usr/local/bin/stats_oled