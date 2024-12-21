import gspread
from google.oauth2.service_account import Credentials
from taiwan_travel import viewpoint, restaurants_crawler ,activities_crawler,hotels_crawler,weather_crawler
from datetime import datetime
# 上傳資料到 Google Sheets
def upload_to_google_sheet(sheet_name, list_data):
    # 設定授權範圍
    scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # 建立憑證
    creds = Credentials.from_service_account_file("/home/ec2-user/Project/google-sheet-api-token.json", scopes=scopes)
    #使用 gspread 連線到 Google Sheet
    client = gspread.authorize(creds)
    # 打開 Google Sheet 
    spreadsheet = client.open_by_key('1Kk7fcTTK9sUSlhAQUpXmtVhysrPhpMoQgcezKYAqP_Q')  # Google Sheets 名稱
    try:
        worksheet = spreadsheet.worksheet(sheet_name)  # 找到活頁簿
    except gspread.exceptions.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=sheet_name, rows="1000", cols="30")  # 新增活頁簿

    worksheet.clear()  # 清空原有資料
    worksheet.update(values=list_data, range_name='A1')  # 更新新資料

# 執行爬蟲並上傳
def main():
    # 取得資料
    try:
        viewpoint_data = viewpoint()
        activities_data = activities_crawler()
        hotels_data = hotels_crawler()
        restaurants_data = restaurants_crawler()
        weather_data = weather_crawler()
    except Exception as e:
        print(f"資料抓取失敗: {e}")
        return

    # 上傳資料到 Google Sheets
    try:
        upload_to_google_sheet("台灣景點",viewpoint_data)
        upload_to_google_sheet("台灣活動", activities_data)
        upload_to_google_sheet("台灣旅館", hotels_data)
        upload_to_google_sheet("台灣餐廳", restaurants_data)
        upload_to_google_sheet("天氣預報", weather_data)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 獲取當前系統時間
        print(f"所有資料成功上傳至 Google Sheets | 時間: {current_time}")       
    except Exception as e:
        print(f"上傳失敗: {e}")

if __name__ == "__main__":
    main()
