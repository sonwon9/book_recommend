from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import urllib.request as req
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

import os
import re
import pickle
import time

book_category_index = ["01", "03", "05", "07", "08", "09", "11", "13", "15", "17", "19", "21", "23", "25", 
                       "26", "27", "29", "31", "32", "33", "35", "38", "39", "41", "42", "47", "50", "53"] # 국내도서 url index

# https://www.whatismybrowser.com/detect/what-is-my-user-agent/ 에서 user_agent를 알아낼 수 있다.
User_Agent = '' # 본인의 user_agent를 입력
chrome_options = Options()
chrome_options.add_argument(f"user-agent={User_Agent }")

for i in tqdm(book_category_index, desc="크롤링하는 카테고리 수"):
    driver = webdriver.Chrome(options=chrome_options)
    url = 'https://product.kyobobook.co.kr/category/KOR/'+i+'#?page=1&type=best&per=20'
    while True:
        try:
            driver.get(url)
            break
        except:
            time.sleep(3)
            pass

    book_titles = []
    book_stories = []
    book_page_urls = []
    book_info = {}

    time.sleep(3)

    for _ in range(1, 50):
        try:
            # 1위책: document.querySelector("#homeTabBest > div.switch_prod_wrap.view_type_list > ol > li:nth-child(1) > div.prod_area.horizontal > div.prod_info_box > div.auto_overflow_wrap.prod_name_group > div > div > a")
            # 2위책: document.querySelector("#homeTabBest > div.switch_prod_wrap.view_type_list > ol > li:nth-child(2) > div.prod_area.horizontal > div.prod_info_box > div.auto_overflow_wrap.prod_name_group > div > div > a")
            for j in range(1, 21):
                page_link = driver.find_element(By.CSS_SELECTOR, '#homeTabBest > div.switch_prod_wrap.view_type_list > ol > li:nth-child('+str(j)+') > div.prod_area.horizontal > div.prod_info_box > div.auto_overflow_wrap.prod_name_group > div > div > a')
                link = page_link.get_attribute('href')
                book_page_urls.append(link)
            
            next_page = driver.find_element(By.CSS_SELECTOR,'#bestBottomPagi > button.btn_page.next')
            next_page.send_keys(Keys.ENTER)
            time.sleep(3)
        except:
            time.sleep(3)
    try:
        for j in range(1, 21):
            page_link = driver.find_element(By.CSS_SELECTOR, '#homeTabBest > div.switch_prod_wrap.view_type_list > ol > li:nth-child('+str(j)+') > div.prod_area.horizontal > div.prod_info_box > div.auto_overflow_wrap.prod_name_group > div > div > a')
            link = page_link.get_attribute('href')
            book_page_urls.append(link)
    except: # 베스트셀러가 1000권 미만인 경우가 있는데 에러 없이 알아서 다음 루프 실행
        pass
    
    for url in tqdm(book_page_urls, desc="책 정보 수집 진행도"):
        try:
            # 책 제목 수집
            # document.querySelector("#contents > div.prod_detail_header > div > div.prod_detail_title_wrap > div > div.prod_title_box.auto_overflow_wrap > div.auto_overflow_contents > div > h1 > span")
            driver.get(url)
            time.sleep(3)
            title = driver.find_element(By.CSS_SELECTOR,'#contents > div.prod_detail_header > div > div.prod_detail_title_wrap > div > div.prod_title_box.auto_overflow_wrap > div.auto_overflow_contents > div > h1 > span')
            book_titles.append(title.text)
        except:
            book_titles.append('')

        try:
            # 책 소개 수집
            story = driver.find_element(By.CSS_SELECTOR,'div.intro_bottom')
            book_stories.append(re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", story.text))
        except:
            book_stories.append('')
    
    driver.quit()
    for j in range(-len(book_titles), 0, -1): # 0에서 len - 1 까지 증가하도록 설계하면 pop 이후 인덱스를 하나 건너뜀 + 후반부에 IndexError 발생
        if not book_titles[j]:
            book_titles.pop(j)
            book_stories.pop(j)
    for j in range(-len(book_stories), 0, -1):
        if not book_stories[j]:
            book_titles.pop(j)
            book_stories.pop(j)
    for j in range(len(book_titles)):
        book_info[book_stories[j]] = book_titles[j]

    filename = "./book_info_dicts/book_info_dict"+i+".p"
    try:
        if book_info:
            with open(filename, "wb") as f:
                pickle.dump(book_info, f)
    except FileNotFoundError:
        os.mkdir("book_info_dicts")
        with open(filename, "wb") as f:
            pickle.dump(book_info, f)