from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

import time
import pyautogui
import pyperclip
import requests
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

driver.get("https://www.naver.com/")
time.sleep(2)

# 쇼핑 클릭
shopping = driver.find_element(By.XPATH, '//*[@id="shortcutArea"]/ul/li[4]/a')
shopping.click()
time.sleep(2)

# 새창을 바라보게 만들기
new_window = driver.window_handles[1]
driver.switch_to.window(new_window)

# 검색어 입력창
serch = driver.find_element(By.XPATH, '//*[@id="gnb-gnb"]/div[2]/div/div[2]/div/div[2]/form/div[1]/div/input')
serch.click()
word = pyperclip.copy("베니하루카")
pyautogui.hotkey("ctrl", "v")
pyautogui.hotkey("enter")
time.sleep(2)

# 리뷰 많은 순 보기
review_up = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[1]/div[1]/div[1]/a[4]')
review_up.click()
time.sleep(2)

def scroll_down():
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


for i in range (1, 5):
    print(f"{i}페이지 입니다.==============================")
    response = requests.get(f'https://search.shopping.naver.com/search/all?adQuery=%EB%B2%A0%EB%8B%88%ED%95%98%EB%A3%A8%EC%B9%B4&frm=NVSHATC&origQuery=%EB%B2%A0%EB%8B%88%ED%95%98%EB%A3%A8%EC%B9%B4&pagingIndex={i}&pagingSize=40&productSet=total&query=%EB%B2%A0%EB%8B%88%ED%95%98%EB%A3%A8%EC%B9%B4&sort=rel&timestamp=&viewType=list')
    
    scroll_down()    

    # 상품 정보 div
    items = driver.find_elements(By.CSS_SELECTOR, ".product_item__MDtDF")
    
    # 파일 생성
    with open(r'C:\work\crawling_practice\가장 맛있는 고구마 찾기\고구마.csv', 'a', encoding='CP949', newline='') as f:
        csvWriter = csv.writer(f)
        
        if i == 1:
            csvWriter.writerow(['상품명', '가격', '링크'])

        for item in items:
            name = item.find_element(By.CSS_SELECTOR, ".product_title__Mmw2K").text
            price = item.find_element(By.CSS_SELECTOR, ".price_num__S2p_v").text
            link = item.find_element(By.CSS_SELECTOR, ".product_link__TrAac").get_attribute("href")

            print(name, price, link)
            csvWriter.writerow([name, price, link])
    