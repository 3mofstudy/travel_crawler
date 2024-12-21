import requests  # 啟用requests模組，用於發送HTTP請求
import pandas as pd


def weather_crawler():
    # 22縣市逐3小時2天 未來鄉鎮預報
    FD = ["F-D0047-001", "F-D0047-005", "F-D0047-009", "F-D0047-013", "F-D0047-017",
          "F-D0047-021", "F-D0047-025", "F-D0047-029", "F-D0047-033", "F-D0047-037",
          "F-D0047-041", "F-D0047-045", "F-D0047-049", "F-D0047-053", "F-D0047-057",
          "F-D0047-061", "F-D0047-065", "F-D0047-069", "F-D0047-073", "F-D0047-077",
          "F-D0047-081", "F-D0047-085"]

    # API授權碼，用於身份驗證
    authorization = "CWA-17EC9EBA-3F32-4CF2-BEC7-61C83F8C45E9"
    # 用來存儲所有資料的空 DataFrame
    AllData = pd.DataFrame()

    # 遍歷每一個資料集ID
    for dataset_id in FD:
        url = url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/{dataset_id}?Authorization={authorization}&format=JSON&elementName=WeatherDescription"

        # 發送請求並解析返回的 JSON 資料
        response = requests.get(url)
        DA = response.json()
        # 用來存儲單次請求的資料
        Towndata = pd.DataFrame()
        # 獲取 Location 的數量
        num_locations = len(DA["records"]["Locations"][0]["Location"])
        # 遍歷每個鄉鎮
        for i in range(num_locations):
            Region = DA["records"]["Locations"][0]["LocationsName"]
            Town = DA["records"]["Locations"][0]["Location"][i]["LocationName"]
            Px = DA["records"]["Locations"][0]["Location"][i]["Longitude"]
            Py = DA["records"]["Locations"][0]["Location"][i]["Latitude"]
            timeDT = pd.DataFrame()
            # 獲取每個鄉鎮中時間的數量
            num_times = len(DA["records"]["Locations"][0]
                            ["Location"][i]["WeatherElement"][9]["Time"])
            # 遍歷每個時間點
            for j in range(num_times):
                startTime = DA["records"]["Locations"][0]["Location"][i]["WeatherElement"][9]["Time"][j]["StartTime"]
                endTime = DA["records"]["Locations"][0]["Location"][i]["WeatherElement"][9]["Time"][j]["EndTime"]
                value = DA["records"]["Locations"][0]["Location"][i]["WeatherElement"][9]["Time"][j]["ElementValue"][0]["WeatherDescription"]
                # 將數據組成單行 DataFrame
                data = pd.DataFrame({
                    "Region": [Region],
                    "Town": [Town],
                    "Px": [Px],
                    "Py": [Py],
                    "開始時間": [startTime],
                    "結束時間": [endTime],
                    "天氣描述": [value]
                })
                timeDT = pd.concat([timeDT, data], ignore_index=True)
            Towndata = pd.concat([Towndata, timeDT], ignore_index=True)
        # 將每次的結果合併到 AllData 中
        AllData = pd.concat([AllData, Towndata], ignore_index=True)
    # 進行天氣描述欄位的分割
    weather_columns = AllData["天氣描述"].str.split("。", expand=True)
    # 設定新的列名
    weather_columns.columns = ["天氣概況", "降雨機率",
                               "預報溫度", "舒適度", "風向風速", "相對溼度", "end0"]
    # 將分割後的欄位合併到原始資料中
    AllData = pd.concat([AllData, weather_columns], axis=1)
    # 天氣參數轉換成純數字
    AllData = AllData.drop(columns=['天氣描述', 'end0'])
    AllData['降雨機率'] = AllData['降雨機率'].str.extract(
        r'(\d+\.?\d*)', expand=False).astype(float)
    AllData['預報溫度'] = AllData['預報溫度'].str.extract(
        r'(\d+\.?\d*)', expand=False).astype(float)
    AllData['相對溼度'] = AllData['相對溼度'].str.extract(
        r'(\d+\.?\d*)', expand=False).astype(float)

    # 將降雨機率為 0 的值設為空格 " "
    AllData['降雨機率'] = AllData['降雨機率'].replace(0, " ")

    # 將 DataFrame 轉換成列表格式
    header = AllData.columns.tolist()
    values = AllData.values.tolist()
    weather_data = [header] + values
    return weather_data
