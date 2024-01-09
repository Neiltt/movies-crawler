# PTT NBA版 爬蟲
import requests
from bs4 import BeautifulSoup
# xlsx引用pandas
import pandas as pd

url = "https://www.ptt.cc/bbs/NBA/index.html"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
respone = requests.get(url, headers=headers)
soup = BeautifulSoup(respone.text, "html.parser")
articles = soup.find_all("div", class_="r-ent")

data_list = []
for a in articles:
    data = {}
    title = a.find("div", class_="title")
    if title and title.a:
        title = title.a.text
    else:
        title = "沒有標題"
    data["標題"] = title

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
    data_list.append(data)

# df一個二維表格，轉換DataFrame格式，匯出xlsx
df = pd.DataFrame(data_list)
df.to_excel("ptt_nba.xlsx", index=False, engine="openpyxl")
print("成功儲存xlsx")


# print(data_list)

    # print(f"標題:{title} 人氣:{popular} 日期:{date}")

# 取網頁資訊
# print(respone.text)
# if respone.status_code == 200:
#     with open('output.html', 'w', encoding='utf-8') as f:
#         f.write(respone.text)
#     print("成功寫入")
# else:
#     print("沒抓到網頁")
