import requests
import json

# 東京都23区の地域コードと名称
tokyo_23ku = {
    "1310100": "千代田区", "1310200": "中央区", "1310300": "港区", "1310400": "新宿区",
    "1310500": "文京区", "1310600": "台東区", "1310700": "墨田区", "1310800": "江東区",
    "1310900": "品川区", "1311000": "目黒区", "1311100": "大田区", "1311200": "世田谷区",
    "1311300": "渋谷区", "1311400": "中野区", "1311500": "杉並区", "1311600": "豊島区",
    "1311700": "北区", "1311800": "荒川区", "1311900": "板橋区", "1312000": "練馬区",
    "1312100": "足立区", "1312200": "葛飾区", "1312300": "江戸川区"
}

# 🚨 警報・注意報（警報以上、重複除去）
def fetch_warnings():
    url = "https://www.jma.go.jp/bosai/warning/data/warning/130000.json"
    try:
        res = requests.get(url)
        data = res.json()
        warnings_by_type = {}
        for area in data.get("areaTypes", [])[0].get("areas", []):
            code = area["code"]
            if code in tokyo_23ku and int(area.get("maxi", 0)) >= 2:
                for warn in area.get("warnings", []):
                    if warn.get("status") == "発表":
                        warn_type = warn.get("name")
                        if warn_type:
                            warnings_by_type.setdefault(warn_type, set()).add(tokyo_23ku[code])
        print("🚨 警報（東京都23区）")
        if warnings_by_type:
            for warn_type, wards in warnings_by_type.items():
                print(f"{warn_type}：{', '.join(sorted(wards))}")
        else:
            print("警報は発表されていません")
    except Exception as e:
        print("警報取得失敗:", e)

# 🌍 地震情報（東京都関連のみ抽出）
def fetch_quake():
    url = "https://www.jma.go.jp/bosai/quake/data/list.json"
    try:
        res = requests.get(url)
        data = res.json()
        print("\n🌍 地震情報（東京都関連）")
        found = False
        for quake in data:
            eq = quake.get("earthquake", {})
            time = quake.get("time", "")
            hypocenter = eq.get("hypocenter", {}).get("name", "")
            max_scale = eq.get("maxScale", "")
            if "東京" in hypocenter or "東京都" in hypocenter:
                print(f"発生時刻: {time}")
                print(f"震源地: {hypocenter}")
                print(f"最大震度: {max_scale}\n")
                found = True
        if not found:
            print("東京都に関連する地震は現在ありません")
    except Exception as e:
        print("地震取得失敗:", e)

# 🌀 台風情報（文章）
def fetch_typhoon():
    url = "https://www.jma.go.jp/bosai/typhoon/data/overview_typhoon.json"
    try:
        res = requests.get(url)
        data = res.json()
        print("\n🌀 台風情報")
        print(data.get("text", "台風情報は現在ありません"))
    except Exception as e:
        print("台風取得失敗:", e)

# ✅ 実行
fetch_warnings()
fetch_quake()
fetch_typhoon()
