import pandas as pd
import requests
import os
from datetime import datetime

# Convert Chinese floor names (e.g. "十層", "三層") to Arabic numbers
_CN_NUM = {
    '零':0,'一':1,'二':2,'三':3,'四':4,'五':5,
    '六':6,'七':7,'八':8,'九':9,'十':10,
    '十一':11,'十二':12,'十三':13,'十四':14,'十五':15,
    '十六':16,'十七':17,'十八':18,'十九':19,'二十':20,
    '二十一':21,'二十二':22,'二十三':23,'二十四':24,'二十五':25,
    '二十六':26,'二十七':27,'二十八':28,'二十九':29,'三十':30,
    '三十一':31,'三十二':32,'三十三':33,'三十四':34,'三十五':35,
    '四十':40,'五十':50,'地下一':'-1','地下二':'-2','地下三':'-3',
}

def cn_floor_to_num(s):
    """Convert '十層' -> '10', '四層' -> '4', etc."""
    if not isinstance(s, str):
        return str(s)
    key = s.replace('層', '').strip()
    return str(_CN_NUM.get(key, s))

# Mapping of target source filenames to the list of townships to be filtered
# Example: "k_lvr_land_b.xls" corresponds to Miaoli County
TARGET_FILES = {
    "k_lvr_land_b.xls": ["頭份市", "竹南鎮"],   # 苗栗縣 頭份,竹南
    "e_lvr_land_b.xls": ["苓雅區", "前鎮區", "新興區", "三民區", "大寮區"],   # 高雄市 前鎮,苓雅,新興,三民,大寮
}

def process_data():
    current_date = datetime.now().strftime("%Y%m%d")
    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    results = []

    for file_name, townships in TARGET_FILES.items():
        # Step 1: Download the source Excel file
        download_url = f"https://plvr.land.moi.gov.tw/Download?fileName={file_name}"
        input_path = f"input/{file_name.replace('.xls', f'_{current_date}.xls')}"

        print(f"📥 Downloading {file_name} ...")
        resp = requests.get(download_url)
        with open(input_path, "wb") as f:
            f.write(resp.content)

        # Step 2: Load the Excel file and filter by specified townships
        df = pd.read_excel(input_path)
        df = df[df['鄉鎮市區'].isin(townships)]

        # Step 3: Retain only the required columns
        cols = [
            '鄉鎮市區', '都市土地使用分區', '交易年月日', '移轉層次', '總樓層數',
            '建物型態', '主要用途', '建物現況格局-房', '建物現況格局-廳',
            '建物現況格局-衛', '建物現況格局-隔間', '總價元', '單價元平方公尺',
            '建物移轉總面積平方公尺', '車位類別', '車位移轉總面積平方公尺', '車位總價元',
            '建案名稱', '棟及號', '備註'
        ]
        df = df[cols]

        # Step 4: Calculate area in ping (1 sqm = 0.3025 ping)
        df['含車位坪數'] = (df['建物移轉總面積平方公尺'] * 0.3025).round(2)
        df['車位坪數'] = (df['車位移轉總面積平方公尺'].fillna(0) * 0.3025).round(2)
        df['不含車位坪數'] = (df['含車位坪數'] - df['車位坪數']).round(2)

        # Step 5: Convert floor to Arabic number
        df['移轉層次'] = df['移轉層次'].apply(cn_floor_to_num)

        # Step 6: Calculate price per ping (萬/坪), rounded to 1 decimal
        # With parking: total price / total area in ping
        df['含車位單價萬坪'] = (df['總價元'] / 10000 / df['含車位坪數']).round(1)
        # Without parking: (total price - parking price) / net area in ping
        net_price = df['總價元'] - df['車位總價元'].fillna(0)
        net_area = df['不含車位坪數'].replace(0, float('nan'))
        df['不含車位單價萬坪'] = (net_price / 10000 / net_area).round(1)

        # Step 6: Export the filtered data to an Excel file
        output_file_key = file_name.replace('.xls', '')
        output_path = f"output/filtered_data_{output_file_key}_{current_date}.xlsx"
        df.to_excel(output_path, index=False, engine='openpyxl')

        # Step 7: Return the first 100 records for display or preview
        records = df.head(100).to_dict(orient='records')
        results.append((output_file_key, records, output_path))

    return results
