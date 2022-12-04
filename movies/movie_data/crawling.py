from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import requests

# JSON
import json

# 크롬 드라이버 세팅용
from webdriver_manager.chrome import ChromeDriverManager

# headless 옵션용
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")


driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
# ↑ 셀레니움이 크롬 드라이브를 잡아서 네이버 영화 페이지 오픈
url = "https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=cnt&date=20221101"

driver.get(url)
time.sleep(1)
# ↑ 그리고 1초 정도 기다려서 페이지가 다 로드되고 나면
# ↓ 거기에 있는 HTML 소스를 다 가져온다.
req = driver.page_source

soup = BeautifulSoup(req, 'html.parser')
# 가져온 소스를 BeautifulSoup에 넣어서 분석할 준비

movies = soup.select('#old_content > table > tbody > tr')

movie_list=[]
http = 'https://movie.naver.com/'
for k, movie in enumerate(movies):
    title = movie.select_one('td.title > div > a')
    if title is not None:
        href = http+title['href']

        driver.execute_script(f"window.open('{href}');")
        driver.switch_to._driver.window_handles[1]
        
        driver.get(href)
        time.sleep(1)
        # ↑ 그리고 1초 정도 기다려서 페이지가 다 로드되고 나면
        # ↓ 거기에 있는 HTML 소스를 다 가져온다.
        req = driver.page_source

        soup = BeautifulSoup(req, 'html.parser')
        # 가져온 소스를 BeautifulSoup에 넣어서 분석할 준비

        poster = soup.select_one('#content > div.article > div.mv_info_area > div.poster > a > img')["src"]
        description = soup.select_one('#content > div.article > div.section_group.section_group_frst > div:nth-child(1) > div > div.story_area > p.con_tx')
        title = title.text
        

        new_data = {"model":"movies.movie"}
        new_data["fields"] = {}
        new_data["fields"]["movie_id"] = k
        new_data["fields"]["title"] = title
        new_data["fields"]["description"] = description
        new_data["fields"]["poster"] = poster
        movie_list.append(new_data)
       
driver.quit()

with open('movies/movie_data/movies.json','w',encoding='UTF-8') as f :
    json.dump(movie_list, f,default=str, ensure_ascii=False, indent=2)