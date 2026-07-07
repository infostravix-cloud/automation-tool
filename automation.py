# automation.py
import datetime
import time
import warnings
import threading
from datetime import datetime
import sys

from faker import Faker
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
import requests as re
import undetected_chromedriver as uc

warnings.filterwarnings('ignore')
fake = Faker('en_IN')
MUTEX = threading.Lock()

proxylist = [
    "192.99.101.142:7497", "198.50.198.93:3128", "52.188.106.163:3128",
    "20.84.57.125:3128", "172.104.13.32:7497", "172.104.14.65:7497",
    "165.225.220.241:10605", "165.225.208.84:10605", "165.225.39.90:10605",
    "165.225.208.243:10012", "172.104.20.199:7497", "165.225.220.251:80",
    "34.110.251.255:80", "159.89.49.172:7497", "165.225.208.178:80",
    "205.251.66.56:7497", "139.177.203.215:3128", "64.235.204.107:3128",
    "165.225.38.68:10605", "165.225.56.49:10605", "136.226.75.13:10605",
    "136.226.75.35:10605", "165.225.56.50:10605", "165.225.56.127:10605",
    "208.52.166.96:5555", "104.129.194.159:443", "104.129.194.161:443",
    "165.225.8.78:10458", "5.161.93.53:1080", "165.225.8.100:10605",
]

def sync_print(text):
    with MUTEX:
        print(text)


def get_driver(proxy):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    options = webdriver.ChromeOptions()
    
    # Streamlit Linux Server ke liye zaroori configurations
    options.add_argument("--headless=new") 
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Streamlit ke Chromium ka path default set karne ke liye (Optional but safe)
    options.binary_location = "/usr/bin/chromium" 

    options.add_argument(f'user-agent={user_agent}')
    options.add_experimental_option("detach", True)
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('use-fake-device-for-media-stream')
    options.add_argument('use-fake-ui-for-media-stream')
    options.add_argument("--disable-extensions")
    
    if proxy is not None:
        options.add_argument(f"--proxy-server={proxy}")
        
    driver = webdriver.Chrome(options=options)
    return driver
# Fixed: Local variables dynamically scope pass ho rahe hain instead of global execution
def start(name, proxy, user, meeting_code, passcode, end_time):
    sync_print(f"{name} started!")
    driver = get_driver(proxy)
    
    try:
        url = f'https://app.zoom.us/wc/join/{meeting_code}'
        sync_print(f"{name} Opening URL: {url}")
        driver.get(url)
        time.sleep(5)
        sync_print(f"{name} Page loaded")
    except Exception as e:
        sync_print(f"{name} Error loading page: {e}")
        try: driver.quit()
        except: pass
        return

    # Passcode enter karo
    try:
        sync_print(f"{name} Looking for passcode field...")
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.ID, 'input-for-pwd'))
        )
        inp2 = driver.find_element(By.ID, 'input-for-pwd')
        inp2.clear()
        inp2.send_keys(passcode)
        sync_print(f"{name} Passcode entered: {passcode}")
        time.sleep(2)
    except Exception as e:
        sync_print(f"{name} Passcode field not found: {e}")

    # Name enter karo
    try:
        sync_print(f"{name} Looking for name field...")
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.ID, 'input-for-name'))
        )
        inp = driver.find_element(By.ID, 'input-for-name')
        inp.clear()
        inp.send_keys(user)
        sync_print(f"{name} Name entered: {user}")
        time.sleep(2)
    except Exception as e:
        sync_print(f"{name} Name field not found: {e}")

    # ====== CAMERA OFF KARO ======
    try:
        sync_print(f"{name} Turning off camera...")
        video_btn = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, '#preview-video-control-button'))
        )
        video_btn.click()
        sync_print(f"{name} Camera turned OFF")
        time.sleep(1)
    except Exception as e:
        sync_print(f"{name} Camera button not found (might already be off): {e}")

    # Join button click karo
    try:
        sync_print(f"{name} Looking for join button...")
        join_btn = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Join')]"))
        )
        join_btn.click()
        sync_print(f"{name} Join button clicked")
        time.sleep(8)
    except Exception as e:
        sync_print(f"{name} Join button error: {e}")
        try:
            btn2 = driver.find_element(By.CLASS_NAME, 'zm-btn')
            btn2.click()
            sync_print(f"{name} Join button clicked (alternate)")
            time.sleep(8)
        except:
            sync_print(f"{name} Could not click join button")

    # Multiple Audio Join Methods
    audio_joined = False
    
    try:
        sync_print(f"{name} Trying audio join method 1...")
        audio_btn = WebDriverWait(driver, 15).until(
            ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Join Audio')]"))
        )
        audio_btn.click()
        sync_print(f"{name} Audio joined (method 1)")
        audio_joined = True
        time.sleep(3)
    except:
        pass
    
    if not audio_joined:
        try:
            sync_print(f"{name} Trying audio join method 2...")
            driver.find_element(By.XPATH, '//*[@id="voip-tab"]/div/button').click()
            sync_print(f"{name} Audio joined (method 2)")
            audio_joined = True
            time.sleep(3)
        except:
            pass
    
    if not audio_joined:
        try:
            sync_print(f"{name} Trying audio join method 3...")
            comp_audio = driver.find_element(By.XPATH, "//button[contains(@class, 'join-audio-by-voip')]")
            comp_audio.click()
            sync_print(f"{name} Audio joined (method 3)")
            audio_joined = True
            time.sleep(3)
        except:
            sync_print(f"{name} All audio join methods failed - might already be in meeting")

    # Mute microphone - Multiple Methods
    try:
        sync_print(f"{name} Trying to mute microphone...")
        mute_btn = WebDriverWait(driver, 8).until(
            ec.element_to_be_clickable((By.XPATH, "//button[@aria-label='Mute my microphone']"))
        )
        mute_btn.click()
        sync_print(f"{name} Microphone muted (method 1)")
        time.sleep(1)
    except:
        try:
            driver.find_element(By.XPATH, '//*[@id="wc-footer"]//button[contains(@class, "audio")]').click()
            sync_print(f"{name} Microphone muted (method 2)")
            time.sleep(1)
        except:
            try:
                driver.find_element(By.CLASS_NAME, 'footer-button__audio-control').click()
                sync_print(f"{name} Microphone muted (method 3)")
                time.sleep(1)
            except:
                sync_print(f"{name} Could not mute - might already be muted or no audio joined")

    try:
        sync_print(f"{name} Ensuring camera is OFF in meeting...")
        video_off = driver.find_element(By.XPATH, "//button[@aria-label='Stop my video']")
        video_off.click()
        sync_print(f"{name} Camera stopped in meeting")
        time.sleep(1)
    except:
        sync_print(f"{name} Camera already OFF or button not found")

    sync_print(f"{name} ✅ Successfully joined meeting! Camera OFF, Mic MUTED")
    sync_print(f"{name} Waiting until time: {end_time}")
    
    # Wait until specified time loop
    while True:
        TimeNow = datetime.now().strftime('%H%M')
        if str(TimeNow) == str(end_time):
            sync_print(f"{name} Time reached, leaving meeting...")
            try:
                driver.quit()
            except:
                pass
            break # Fixed: sys.exit() ya exit() explicitly backend process kill karta tha, ab break karega.
        time.sleep(30)


# This is exactly what Flask's application endpoint `run_zoom_automation` relies on!
def run_zoom_automation(number, meeting_code, passcode, end_time):
    workers = []
    for i in range(int(number)):
        try:
            proxy = proxylist[i]
        except IndexError:
            proxy = None
            
        user = fake.name()
        
        # Template rules: Anti-CAPTCHA pacing delays between bot spins
        if i > 0:
            time.sleep(10)
            
        wk = threading.Thread(
            target=start, 
            args=(f'[Thread_{i+1}]', proxy, user, meeting_code, passcode, end_time)
        )
        workers.append(wk)
        wk.start()
        
    for wk in workers:
        wk.join()