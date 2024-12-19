import pandas as pd
from datetime import datetime

# 資料來源 URL
def restaurants_crawler():
    #Download website
    url = "https://media.taiwan.net.tw/XMLReleaseALL_public/Restaurant_C_f.csv"

    # 記錄爬取時間
    CrawlerTime = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 爬取資料
    DT = pd.read_csv(url)

    # 確認所需欄位
    required_columns = ["Name","Tel","Add","Region","Town","Opentime","Px","Py","Parkinginfo"]
    missing_columns = [col for col in required_columns if col not in DT.columns]
    if missing_columns:
        print(f"Missing columns:{missing_columns}")
        return None
    #選取需要的欄位，加入時間戳
    DA = DT[required_columns].copy()   #use copy 確保安全
    DA['CrawlerTime'] = CrawlerTime  #加入時間欄位

    #替換NaN 和 inf 值
    DA = DA.fillna('').replace([float('inf'),float('-inf')],'')

    # 將 DataFrame 轉換成列表格式
    header = DA.columns.tolist()
    values = DA.values.tolist()
    restaurants_data = [header] + values

    return restaurants_data









