from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

import time
import pyautogui
import pyperclip
import csv

# 브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러 메세지 없애기
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 웹페이지 해당 주소 이동
driver.implicitly_wait(5)  # 웹페이지가 로딩 될때까지 5초 기다림
driver.maximize_window()  # 화면 최대화

driver.get("https://shopping.naver.com/home")

# 검색어 입력창
serch = driver.find_element(
    By.CSS_SELECTOR,
    "#gnb-gnb > div._gnb_header_area_150KE > div > div._gnbLogo_gnb_logo_3eIAf > div > div._gnbSearch_gnb_search_3O1L2 > form > div._gnbSearch_inner_2Zksb > div > input",
)
serch.click()
pyperclip.copy("크록스")
pyautogui.hotkey("ctrl", "v")
pyautogui.hotkey("enter")
time.sleep(2)

# 스크롤 전 높이
before_h = driver.execute_script("return window.scrollY")

# 무한 스크롤
while True:
    # 맨 아래로 스크롤 내리기
    driver.find_element(By.CSS_SELECTOR, "body")
    pyautogui.hotkey("END")

    # 스크롤 사이 페이지 로딩 시간
    time.sleep(1)

    # 스크롤 후 높이
    after_h = driver.execute_script("return window.scrollY")

    if after_h == before_h:
        break
    before_h = after_h

# 파일 생성
f = open(r'C:\work\crawling_practice\네이버 쇼핑 크롤링\data.csv', 'w', encoding='CP949', newline='')
csvWriter = csv.writer(f)

# 상품 정보 div
items = driver.find_elements(By.CSS_SELECTOR, ".product_item__MDtDF")

for item in items:
    name = item.find_element(By.CSS_SELECTOR, ".product_title__Mmw2K").text
    price = item.find_element(By.CSS_SELECTOR, ".price_num__S2p_v").text
    link = item.find_element(By.CSS_SELECTOR, ".product_link__TrAac").get_attribute("href")
    print(name, price, link)
    
    csvWriter.writerow([name, price, link])

# 파일 닫기 
f.close()
