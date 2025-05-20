# process_data.py
import pandas as pd
import requests
import os
from datetime import datetime

def process_data():
    # 1. 下載原始檔案
    os.makedirs("input", exist_ok=True)
    
    # 使用當前日期作為檔案名
    current_date = datetime.now().strftime("%Y%m%d")
    filename = f"input/k_lvr_land_b_{current_date}.xls"
    download_url = 'https://plvr.land.moi.gov.tw//Download?fileName=k_lvr_land_b.xls'
    resp = requests.get(download_url)
    with open(filename, "wb") as f:
        f.write(resp.content)

    # 2. 讀取並過濾
    df = pd.read_excel(filename)
    df = df[df['鄉鎮市區'].isin(['頭份市', '竹南鎮'])]

    # 3. 只保留指定欄位，並依你要求的順序
    cols = [
        '鄉鎮市區', '都市土地使用分區', '交易年月日', '移轉層次', '總樓層數',
        '建物型態', '主要用途', '建物現況格局-房', '建物現況格局-廳',
        '建物現況格局-衛', '建物現況格局-隔間', '總價元', '單價元平方公尺',
        '車位類別', '車位總價元', '建案名稱', '棟及號'
    ]
    df = df[cols]

    # 4. 寫成新的 Excel，讓 Bot 附件傳送
    out_dir = 'output'
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f'filtered_data_{current_date}.xlsx')
    df.to_excel(out_path, index=False, engine='openpyxl')

    # 5. 取前 5 筆作為 Embed 顯示
    records = df.head(20).to_dict(orient='records')

    return records, out_path
