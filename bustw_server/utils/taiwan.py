class Taiwan:
    def __init__(self):
        self.__cities = {
            "Keelung": {
                "name": "基隆市",
                "code": "City/Keelung"
            },
            "NewTaipei": {
                "name": "新北市",
                "code": "City/NewTaipei"
            },
            "Taipei": {
                "name": "台北市",
                "code": "City/Taipei"
            },
            "YilanCounty": {
                "name": "宜蘭縣",
                "code": "City/YilanCounty"
            },
            "Taoyuan": {
                "name": "桃園市",
                "code": "City/Taoyuan"
            },
            "Hsinchu": {
                "name": "新竹市",
                "code": "City/Hsinchu"
            },
            "HsinchuCounty": {
                "name": "新竹縣",
                "code": "City/HsinchuCounty"
            },
            "MiaoliCounty": {
                "name": "苗栗縣",
                "code": "City/MiaoliCounty"
            },
            "Taichung": {
                "name": "台中市",
                "code": "City/Taichung"
            },
            "ChanghuaCounty": {
                "name": "彰化縣",
                "code": "City/ChanghuaCounty"
            },
            "NantouCounty": {
                "name": "南投縣",
                "code": "City/NantouCounty"
            },
            "YunlinCounty": {
                "name": "雲林縣",
                "code": "City/YunlinCounty"
            },
            "Chiayi": {
                "name": "嘉義市",
                "code": "City/Chiayi"
            },
            "ChiayiCounty": {
                "name": "嘉義縣",
                "code": "City/ChiayiCounty"
            },
            "Tainan": {
                "name": "台南市",
                "code": "City/Tainan"
            },
            "Kaohsiung": {
                "name": "高雄市",
                "code": "City/Kaohsiung"
            },
            "PingtungCounty": {
                "name": "屏東縣",
                "code": "City/PingtungCounty"
            },
            "TaitungCounty": {
                "name": "台東縣",
                "code": "City/TaitungCounty"
            },
            "HualienCounty": {
                "name": "花蓮縣",
                "code": "City/HualienCounty"
            },
            "PenghuCounty": {
                "name": "澎湖縣",
                "code": "City/PenghuCounty"
            },
            "KinmenCounty": {
                "name": "金門縣",
                "code": "City/KinmenCounty"
            },
            "LienchiangCounty": {
                "name": "連江縣",
                "code": "City/LienchiangCounty"
            },
            "InterCity": {
                "name": "公路客運",
                "code": "InterCity"
            }
        }

    @property
    def cities(self) -> dict:
        return self.__cities


taiwan = Taiwan()
