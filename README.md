# bustw_server

bus tracker for Taiwanese Server

## API

> /info/{City}

取得特定縣市之公車路線資料。

| Parameter | Value            |
| --------- | ---------------- |
| City      | 城市名稱（英文） |

> /stop/{City}/{Route}

取得特定縣市之特定公車站序資料。

| Parameter | Value            |
| --------- | ---------------- |
| City      | 城市名稱（英文） |
| Route     | 路線名稱         |

## Usage

```shell
# Install requirements
pip3 install -r requirements.txt

# Start
python3 app.py
```

## Available Cities

1. 基隆市：`Keelung`
2. 新北市：`NewTaipei`
3. 台北市：`Taipei`
4. 宜蘭縣：`YilanCounty`
5. 桃園市：`Taoyuan`
6. 新竹市：`Hsinchu`
7. 新竹縣：`HsinchuCounty`
8. 苗栗縣：`MiaoliCounty`
9. 台中市：`Taichung`
10. 彰化縣：`ChanghuaCounty`
11. 南投縣：`NantouCounty`
12. 雲林縣：`YunlinCounty`
13. 嘉義市：`Chiayi`
14. 嘉義縣：`ChiayiCounty`
15. 台南市：`Tainan`
16. 高雄市：`Kaohsiung`
17. 屏東縣：`PingtungCounty`
18. 台東縣：`TaitungCounty`
19. 花蓮縣：`HualienCounty`
20. 澎湖縣：`PenghuCounty`
21. 金門縣：`KinmenCounty`
22. 連江縣：`LienchiangCounty`
23. 公路客運：`InterCity`
