import pandas as pd
import requests
import os
from datetime import datetime

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
            '車位類別', '車位總價元', '建案名稱', '棟及號','備註'
        ]
        df = df[cols]

        # Step 4: Export the filtered data to an Excel file
        output_file_key = file_name.replace('.xls', '')
        output_path = f"output/filtered_data_{output_file_key}_{current_date}.xlsx"
        df.to_excel(output_path, index=False, engine='openpyxl')

        # Step 5: Return the first 100 records for display or preview
        records = df.head(100).to_dict(orient='records')
        results.append((output_file_key, records, output_path))

    return results
