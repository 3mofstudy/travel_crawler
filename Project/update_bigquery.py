import pandas as pd
from urllib.parse import quote
from google.cloud import bigquery
from google.api_core.exceptions import NotFound  # 正確的 NotFound 位置
import os

# 設定 Google Cloud 認證環境變數
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-sheet-api-token.json"


# 初始化 BigQuery 客戶端
client = bigquery.Client(project="homework-441203")

# 設定資料集的名稱
dataset_id = "taiwan_travel"

# 檢查資料集是否存在，若不存在則創建
dataset_ref = client.dataset(dataset_id)

try:
    # 檢查資料集是否存在
    client.get_dataset(dataset_ref)
    print(f"資料集 {dataset_id} 已存在。")
except NotFound:  # 使用 google.api_core.exceptions.NotFound
    # 若資料集不存在，則創建資料集
    dataset = bigquery.Dataset(dataset_ref)
    dataset = client.create_dataset(dataset)  # 創建資料集
    print(f"資料集 {dataset_id} 已創建。")





# Google Sheet 的 ID
sheet_id = "1Kk7fcTTK9sUSlhAQUpXmtVhysrPhpMoQgcezKYAqP_Q"

# 分頁名稱與 type 的對應
tabs = {
    "台灣景點": "景點",
    "台灣活動": "活動",
    "台灣旅館": "旅館",
    "台灣餐廳": "餐廳"
}

# 存放所有分頁數據的列表
dataframes = []

# 逐個分頁讀取資料，並添加 type 欄位
for tab_name, tab_type in tabs.items():
    # 將分頁名稱進行 URL 編碼
    encoded_tab_name = quote(tab_name)
    
    # 生成分頁的 CSV 下載連結
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={encoded_tab_name}"
    
    # 讀取數據並選取指定的欄位
    df = pd.read_csv(csv_url, usecols=["Region", "Town", "Py", "Px"])
    
    # 移除 'Region' 欄位為空白的資料行
    df = df.dropna(subset=["Region"])
    
    # 新增 'type' 欄位，並設置為中文類型名稱
    df["type"] = tab_type
    
    # 添加到數據列表中
    dataframes.append(df)

# 合併所有分頁的數據
combined_df = pd.concat(dataframes, ignore_index=True)

# 顯示合併後的數據
#print(combined_df)

# 上傳到 BigQuery
project_id = "homework-441203"  # 你的專案 ID
dataset_id = "taiwan_travel"    # BigQuery 中的 Dataset 名稱
table_id = "places_data"        # BigQuery 中的 Table 名稱

# 初始化 BigQuery 客戶端
client = bigquery.Client(project=project_id)

# 設定 BigQuery 資料表的完整名稱
table_ref = f"{project_id}.{dataset_id}.{table_id}"

# 將 DataFrame 上傳到 BigQuery
job = client.load_table_from_dataframe(combined_df, table_ref)

# 等待上傳完成
job.result()

print(f"資料已成功上傳到 BigQuery: {table_ref}")
