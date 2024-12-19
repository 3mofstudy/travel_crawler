import pandas as pd
from datetime import datetime


def hotels_crawler():
    # 網頁下載點
    urls = "https://media.taiwan.net.tw/XMLReleaseALL_public/Hotel_C_f.csv"

    # 記錄爬取時間
    CrawlerTime = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 爬取資料
    DT = pd.read_csv(urls)

    # 確認所需欄位是否存在
    required_columns = ["Name", "Tel", "Add", "Region","Website",
                        "Town", "Px", "Py", "Parkinginfo", "Serviceinfo"]
    missing_columns = [
        col for col in required_columns if col not in DT.columns]

    # 檢查是否有缺少的欄位
    if missing_columns:
        print(f"Missing columns: {missing_columns}")
        return None

    # 選取需要的欄位，並加入時間戳
    DA = DT[required_columns].copy()  # 使用 copy 確保安全
    DA['CrawlerTime'] = CrawlerTime  # 加入時間欄位

    # 替換 NaN 和 inf 值
    DA = DA.fillna('').replace([float('inf'), float('-inf')], '')

    # 將 DataFrame 轉換為列表格式
    header = DA.columns.tolist()
    values = DA.values.tolist()
    data = [header] + values

    return data
