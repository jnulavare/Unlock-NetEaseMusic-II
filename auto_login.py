# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "005A3D7DC9AA5D8D4B44DC6444007B8177092EEF252AEEBE86F3BD210BCCBBA1658F49F592F4E24657DEC6FBA6E9408881F9054A0217CECA5C57B74E9C5BB8C15AEC9B21E4386A4D136AD603C4994532F2C164EF40AADE6E85B9DC47DEA36EA998D4CA6FD59265C50A1948340EBCFDEADF7884E1C184079AC46F1675636EEF3ABCAA3722BEFD538462612493625655CED93EE00F186061AC9459750AC220FE041FBAFE522651C6E14EA75DBB939D6740B58CE5EAB2E3BD35FDD065BCA7E2A28FB214EBE1C5D051548B6E5FBBA1F88153F80C7E0A771E6C874749D1D32E430989F205EB47BB10991717FA4F3DE4F2E7D3A05115846FC50DE9C8409431F2AB325E205372E45AC8C32838E2EADDD8CDB9B207D768985DF415A50DA0C538CA73A65FA683CFABA48E83ED6DF2952333952ED40ED17FDBFA75A587DC10D74E3E3D9006D691ED7737C32373F3522553774EFB6106ADFA6019162D05E4927F42AE9F7E52A36584004791F8A7E8512F8DA6849F9D572277492BD339C00E3C3514071516B88DDAF7E8787F39C3C10091D468A9E97408"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
