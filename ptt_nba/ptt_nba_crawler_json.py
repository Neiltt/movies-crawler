# PTT NBA版 爬蟲
# 分別引用HTTP模組、分析網頁的HTML模組
import requests
from bs4 import BeautifulSoup
import json

# 透過Url進入、帶入User-Agent參數在headers、html.parser取得html資訊
url = "https://www.ptt.cc/bbs/NBA/index.html"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
respone = requests.get(url, headers=headers)
soup = BeautifulSoup(respone.text, "html.parser")
articles = soup.find_all("div", class_="r-ent")

# 網頁觀察html，從整個主題塊逐行取得資料
data_list = []
for a in articles:
    # 建立空字典，依序寫入key value塞進[]，if else防呆
    data = {}
    title = a.find("div", class_="title")
    if title and title.a:
        title = title.a.text
    else:
        title = "沒有標題"
    data["標題"] = title
    # print(title)

    popular = a.find("div", class_="nrec")
    if popular and popular.span:
        popular = popular.span.text
    else:
        popular = "N/A"
    data["人氣"] = popular

    date = a.find("div", class_="date")
    if date:
        date = date.text
    else:
        date = "N/A"
    data["日期"] = date
    # print(f"標題:{title} 人氣:{popular} 日期:{date}")
    data_list.append(data)

# 另存json檔案
# ensure_ascii: 保留非 ASCII 字符(中文、日文)、True非 ASCII 字符轉換為 Unicode 編碼
with open("ptt_nba_data.json", "w", encoding="utf-8") as file:
    json.dump(data_list, file, ensure_ascii=False, indent=4)
print("成功儲存json")

# 取網頁資訊狀態，寫入html檔案
# print(respone.text)
# if respone.status_code == 200:
#     with open('output.html', 'w', encoding='utf-8') as f:
#         f.write(respone.text)
#     print("成功寫入")
# else:
#     print("沒抓到網頁")