import pandas as pd
from datetime import datetime

def activities_crawler():
    # 網頁下載點
    urls = "https://media.taiwan.net.tw/XMLReleaseALL_public/Activity_C_f.csv"

    # 記錄爬取時間
    CrawlerTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 爬取資料
    DT = pd.read_csv(urls)

    # 確認所需欄位是否存在
    required_columns = ["Name",  "Add", "Region", "Town", "Org", "Start", "End", "Px", "Py"]
    missing_columns = [col for col in required_columns if col not in DT.columns]
    if missing_columns:
        print(f"Missing columns: {missing_columns}")
        return None

    # 選取需要的欄位，並加入時間戳
    DA = DT[required_columns].copy()  # 使用 copy 確保安全
    DA['CrawlerTime'] = CrawlerTime  # 加入時間欄位

    # 確保 End 和 CrawlerTime 都是日期時間格式
    try:
        DA['End'] = pd.to_datetime(DA['End'], errors='coerce')  # 處理無效的日期
        DA['CrawlerTime'] = pd.to_datetime(DA['CrawlerTime'])
    except Exception as e:
        print(f"Error parsing datetime: {e}")
        return None

    # 篩選 End > CrawlerTime 的行
    DA = DA[DA['End'] > DA['CrawlerTime']]

    # 填補缺失值並移除無效值
    DA = DA.fillna('').replace([float('inf'), float('-inf')], '')

    # 將日期時間轉換為字串格式（避免 Timestamp 無法序列化）
    for col in ['End', 'CrawlerTime']:
        if col in DA.columns:
            DA[col] = DA[col].dt.strftime("%Y-%m-%d %H:%M:%S")  # 轉換為字串格式

    # 將 DataFrame 轉換為列表格式
    header = DA.columns.tolist()
    values = DA.values.tolist()
    activities_data = [header] + values

    return activities_data
