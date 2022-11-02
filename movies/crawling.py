from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import requests
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
# driver.quit()

soup = BeautifulSoup(req, 'html.parser')
# 가져온 소스를 BeautifulSoup에 넣어서 분석할 준비

movies = soup.select('#old_content > table > tbody > tr')

http = 'https://movie.naver.com/'
for movie in movies:
    title = movie.select_one('td.title > div > a')
    if title is not None:
        path = http+title['href']
        print(title.text)
        print(path)


# from selenium import webdriver
# from bs4 import BeautifulSoup
# import time
# from selenium.common.exceptions import NoSuchElementException
# from pymongo import MongoClient
# import requests
# # 크롬 드라이버 세팅용
# from webdriver_manager.chrome import ChromeDriverManager

# # headless 옵션용
# from selenium.webdriver.chrome.options import Options

# chrome_options = Options()
# chrome_options.add_argument("--headless")

# driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
# # ↑ 셀레니움이 크롬 드라이브를 잡아서 네이버 영화 페이지 오픈
# url = "https://movie.naver.com//movie/bi/mi/basic.naver?code=196548"

# driver.get(url)
# time.sleep(1)
# # ↑ 그리고 1초 정도 기다려서 페이지가 다 로드되고 나면
# # ↓ 거기에 있는 HTML 소스를 다 가져온다.
# req = driver.page_source
# driver.quit()

# soup = BeautifulSoup(req, 'html.parser')
# # 가져온 소스를 BeautifulSoup에 넣어서 분석할 준비

# poster = soup.select_one('#content > div.article > div.mv_info_area > div.poster > a > img')["src"]
# print(poster)