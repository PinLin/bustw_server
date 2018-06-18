#! /usr/bin/env python3

# 城市在 API 中的名稱對應表
MAPS = {
    # 基隆市
    "Keelung": "City/Keelung",
    # 新北市
    "NewTaipei": "City/NewTaipei",
    # 台北市
    "Taipei": "City/Taipei",
    # 宜蘭縣
    "YilanCounty": "City/YilanCounty",
    # 桃園市
    "Taoyuan": "City/Taoyuan",
    # 新竹市
    "Hsinchu": "City/Hsinchu",
    # 新竹縣
    "HsinchuCounty": "City/HsinchuCounty",
    # 苗栗縣
    "MiaoliCounty": "City/MiaoliCounty",
    # 台中市
    "Taichung": "City/Taichung",
    # 彰化縣
    "ChanghuaCounty": "City/ChanghuaCounty",
    # 南投縣
    "NantouCounty": "City/NantouCounty",
    # 雲林縣
    "YunlinCounty": "City/YunlinCounty",
    # 嘉義市
    "Chiayi": "City/Chiayi",
    # 嘉義縣
    "ChiayiCounty": "City/ChiayiCounty",
    # 台南市
    "Tainan": "City/Tainan",
    # 高雄市
    "Kaohsiung": "City/Kaohsiung",
    # 屏東縣
    "PingtungCounty": "City/PingtungCounty",
    # 台東縣
    "TaitungCounty": "City/TaitungCounty",
    # 花蓮縣
    "HualienCounty": "City/HualienCounty",
    # 澎湖縣
    "PenghuCounty": "City/PenghuCounty",
    # 金門縣
    "KinmenCounty": "City/KinmenCounty",
    # 連江縣
    "LienchiangCounty": "City/LienchiangCounty",
    # 公路客運
    "InterCity": "InterCity",
}