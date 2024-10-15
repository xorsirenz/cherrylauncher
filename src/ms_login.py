#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import minecraft_launcher_lib
import subprocess
import sys

REDIRECT_URL = "https://login.live.com/oauth20_desktop.srf"
CLIENT_ID = "8e959dc7-8131-4ad0-b5e2-bd856e177263"

def login():
    login_url, state, code_verifier = minecraft_launcher_lib.microsoft_account.get_secure_login_data(CLIENT_ID, REDIRECT_URL)
    driver = webdriver.Firefox()
    driver.get(login_url)
    
    try:
        WebDriverWait(driver, 300).until(
                EC.url_contains(REDIRECT_URL))
    finally:
        code_url = driver.current_url
        driver.quit()
        try:
            auth_code = minecraft_launcher_lib.microsoft_account.parse_auth_code_url(code_url, state)
        except AssertionError:
            print("states do not match")
            sys.exit(1)
        except KeyError:
            print("url is not valid")
            sys.exit(1)

        login_data = minecraft_launcher_lib.microsoft_account.complete_login(CLIENT_ID, None, REDIRECT_URL, auth_code, code_verifier)
        return login_data
