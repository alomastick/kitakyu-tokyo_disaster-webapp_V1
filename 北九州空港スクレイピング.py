#C:\Users\aloma\AppData\Local\Programs\Microsoft VS Code　にある

import requests
from bs4 import BeautifulSoup

URL = "https://www.kitakyu-air.jp"
response = requests.get(URL)
response = requests.get(URL)
print("HTML取得完了")

soup = BeautifulSoup(response.content, "html.parser")
soup = BeautifulSoup(response.content, "html.parser")
print("HTML解析完了")

table = soup.find("table", id="dd")
table = soup.find("table", id="dd")
print("テーブル取得完了")
if table is None:
    print("テーブルが見つかりませんでした")
    exit()

rows = table.find_all("tr", class_="ff-small")
rows = table.find_all("tr", class_="ff-small")
print(f"{len(rows)} 行取得")

flights = []

for row in rows:
    cols = row.find_all("td")
    if len(cols) == 1 and "フライトは終了" in cols[0].text:
        continue
    if len(cols) == 7:
        flight = {
            "航空会社": cols[0].text.strip(),
            "便名": cols[1].text.strip(),
            "行先": cols[2].text.strip(),
            "定刻": cols[3].text.strip(),
            "変更": cols[4].text.strip(),
            "ゲート": cols[5].text.strip(),
            "備考": cols[6].text.strip()
        }
        flights.append(flight)

for f in flights:
    print(f)

import json

with open("flights.json", "w", encoding="utf-8") as f:
    json.dump(flights, f, ensure_ascii=False, indent=2)