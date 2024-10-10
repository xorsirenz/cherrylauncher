import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#https://gist.github.com/dewycube/223d4e9b3cddde932fbbb7cfcfb96759
url = "https://login.live.com/oauth20_authorize.srf?client_id=00000000402B5328&redirect_uri=https://login.live.com/oauth20_desktop.srf&response_type=code&scope=service::user.auth.xboxlive.com::MBI_SSL"
redirect_url = "https://login.live.com/oauth20_desktop.srf?code="

def login():
    driver = webdriver.Firefox()
    driver.get(url)
    
    try:
        WebDriverWait(driver, 300).until(
                EC.url_contains(redirect_url))
    finally:
        print(driver.current_url)
        code = driver.current_url.split("code=")[1].split("&")[0]
        print(code)
        driver.quit()

        # minecraft launcher
        r = requests.post("https://login.live.com/oauth20_token.srf", data = {
            "client_id": "00000000402B5328",
            "scope": "service::user.auth.xboxlive.com::MBI_SSL",
            "code": code,
            "redirect_uri": "https://login.live.com/oauth20_desktop.srf",
            "grant_type": "authorization_code"
        })
        microsoft_token = r.json()["access_token"]
        microsoft_refresh_token = r.json()["refresh_token"]

        # xbl token
        r = requests.post("https://user.auth.xboxlive.com/user/authenticate", json = {
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": microsoft_token
            },
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT"
        })
        xbl_token = r.json()["Token"]
 
        # xsts token
        r = requests.post("https://xsts.auth.xboxlive.com/xsts/authorize", json = {
            "Properties": {
                "SandboxId": "RETAIL",
                "UserTokens": [xbl_token]
            },
            "RelyingParty": "rp://api.minecraftservices.com/",
            "TokenType": "JWT"
        })
        xsts_userhash = r.json()["DisplayClaims"]["xui"][0]["uhs"]
        xsts_token = r.json()["Token"]
    
        # minecraft token
        r = requests.post("https://api.minecraftservices.com/authentication/login_with_xbox", json = {
            "identityToken": f"XBL3.0 x={xsts_userhash};{xsts_token}"
        })
        minecraft_token = r.json()["access_token"]

        # minecraft username and uuid
        r = requests.get("https://api.minecraftservices.com/minecraft/profile", headers = {
            "Authorization": f"Bearer {minecraft_token}"
        })
        username = r.json()["name"]
        uuid = r.json()["id"]

        r = requests.post("https://login.live.com/oauth20_token.srf", data = {
            "scope": "service::user.auth.xboxlive.com::MBI_SSL",
            "client_id": "00000000402B5328",
            "grant_type": "refresh_token",
            "refresh_token": microsoft_refresh_token
        })
        microsoft_token = r.json()["access_token"]
        return username, uuid, microsoft_token

