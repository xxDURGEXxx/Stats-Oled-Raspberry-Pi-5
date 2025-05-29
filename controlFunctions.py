import subprocess
import socket
import re
import configparser
import os

BYTES_IN_GB = 1073741824
SCREEN_MAX_Y = 64
SCREEN_MAX_X = 128

app_conf = configparser.ConfigParser()
config_path = "/etc/stats_oled/config.ini"
if not os.path.exists(config_path):
    config_path = "config/config.ini"  # Fallback for devs
app_conf.read(config_path)

WLAN_INTERFACE = app_conf.get("general","wlan",fallback="wlan0")

def check_interface_status(timeout=1):
    ip_last = None
    full_ip = None
    # Step 1: Check if interface is connected to a router (has IP)
    try:
        output = subprocess.check_output(["ip", "addr", "show", WLAN_INTERFACE]).decode()
        match = re.search(r"inet (\d+\.\d+\.(\d+\.\d+))", output)

        if match:
            connected_to_router = True
            full_ip = match.group(1)
            ip_last = match.group(2)  # Last number of IP
        else:
            connected_to_router = False
    except:
        return "disconnected", None ,None

    # Step 2: Check internet access
    if connected_to_router:
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
            return "internet", full_ip , ip_last 
        except:
            return "no_internet", full_ip, ip_last

    return "disconnected", None ,None


def get_wireless_quality():
    try:
        output = subprocess.check_output(["iwconfig", WLAN_INTERFACE]).decode()

        link_match = re.search(r"Link Quality=(\d+)/(\d+)", output)
        signal_match = re.search(r"Signal level=(\d+)/(\d+)", output)
        bit_rate_match = re.search(r"Bit Rate[:=](\d+(?:\.\d+)?)\s*Mb/s", output)
        ssid_match = re.search(r'ESSID:"([^"]+)"', output)


        if link_match and signal_match and bit_rate_match and ssid_match:
            link = int(link_match.group(1)) * 100 // int(link_match.group(2))
            signal = int(signal_match.group(1)) * 100 // int(signal_match.group(2))
            bit_rate =bit_rate_match.group(1)
            ssid=ssid_match.group(1)
            return {
                "link_quality": link,
                "signal_level": signal,
                "bit_rate": bit_rate,
                "ssid": ssid
            }
    except:
        pass
    return None


def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return round(int(f.read()) / 1000.0, 1)
    except:
        return 'err'

def get_nvme_temp():
    try:
        with open("/sys/class/nvme/nvme0/hwmon1/temp1_input") as f:
            return round(int(f.read()) / 1000, 1)  # convert to °C, 2 decimal places
    except Exception:
        return "err"

def get_rp1_temp():
    try:
        with open("/sys/class/hwmon/hwmon2/temp1_input", "r") as f:
            return round(int(f.read()) / 1000.0, 1)
    except:
        return 'err'

def get_pmic_temp():
    try:
        output = subprocess.check_output(["vcgencmd", "measure_temp", "pmic"]).decode()
        temp_str = output.strip().replace("temp=", "").replace("'C", "")
        return float(temp_str)
    except Exception:
        return "err"
    

import glob

def get_average_cpu_frequency_mhz():
    freqs = []
    cpu_freq_paths = glob.glob("/sys/devices/system/cpu/cpu[0-9]*/cpufreq/scaling_cur_freq")
    
    for path in cpu_freq_paths:
        try:
            with open(path, "r") as f:
                freq = int(f.read().strip())
                freqs.append(freq)
        except:
            continue

    if freqs:
        avg_mhz = sum(freqs) // (1000 * len(freqs))
        return avg_mhz
    return None
