import pandas as pd
from urllib.parse import quote  # 引入 URL 編碼工具

# Google Sheet 的 ID
sheet_id = "1Kk7fcTTK9sUSlhAQUpXmtVhysrPhpMoQgcezKYAqP_Q"

# 分頁名稱與 type 的對應
tabs = {
    "台灣景點": "view",
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
    df = pd.read_csv(csv_url, usecols=["Name","Region", "Town", "Py", "Px"])
    
    # 移除 'Region' 欄位為空白的資料行
    df = df.dropna(subset=["Region"])
    
    # 新增 'type' 欄位
    df["type"] = tab_type
    
    # 添加到數據列表中
    dataframes.append(df)

# 合併所有分頁的數據
combined_df = pd.concat(dataframes, ignore_index=True)

# 顯示合併後的數據
print(combined_df)


# 保存到上一個目錄的 CSV 文件

combined_df.to_csv("../taiwan_travel.csv", index=False)
