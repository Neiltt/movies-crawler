# 查找年度好評電影，匯出易閱讀格式，省下選擇猶豫時間。
# 透過Python的requests 和 BeautifulSoup 模組，動態爬取資訊，pandas轉換閱讀格式
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# List[]放置爬取內容，網頁請求parser網頁，觀察網頁爬取資料
data_list = []
def fetch_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    movies = soup.find_all("div", class_="lister-list")
    for movie in movies:
        details = movie.find_all("div", class_="lister-item mode-detail")
        for detail in details:
            contents = detail.find_all("div", class_="lister-item-content")
            for content in contents:
                name = content.find("h3", class_="lister-item-header")
                name = name.a.text.strip() #去掉空白

                # 取時長span，三元判斷runtime_span
                runtime_span = content.find("span", class_="runtime")
                runtime = runtime_span.text.strip() if runtime_span else None  # Extract text and handle potential absence

                # 取星級評分，部分空值需保護判斷
                rating_span = content.find("div", class_="ipl-rating-widget")
                if rating_span:
                    small_rating_div = rating_span.find("div", class_="ipl-rating-star small")
                    if small_rating_div:
                        rating_star = small_rating_div.find("span", class_="ipl-rating-star__rating")
                        if rating_star:
                            star = rating_star.text.strip()

                # print(f"Name: {name}, Runtime: {runtime}, Star: {star}")

                data_list.append([name, runtime, star])
    print(data_list)

# 換頁標籤，連結防呆，處理兩個上下頁的連結
    next_page = soup.find("div", class_="list-pagination")
    if next_page and next_page.a:
        # next_url = next_page.a.get("href")
        next_urls = next_page.find_all("a")
        next_url = next_urls[1].get("href")
        print(f"正在爬取:{next_url}")
        time.sleep(1)
        urlmain = "https://www.imdb.com"
        fetch_data(urlmain+next_url)




    # print(soup)

url = "https://www.imdb.com/list/ls562521060/"
fetch_data(url)

# xlsx標頭設定
df = pd.DataFrame(data_list, columns=["電影名稱", "電影時長", "評價"])
df.to_excel("電影排行.xlsx", index=False, engine="openpyxl") #第一欄index索引