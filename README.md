# [Deprecated] bustw_server

My new project for this purpose is here. https://github.com/PinLin/bustw-server

bus tracker for Taiwanese Server

## Usage
1. Clone.
   ```bash
   git clone https://github.com/PinLin/bustw_server
   cd bustw_server
   ```

2. Install dependencies.
   ```bash
   pip3 install -r requirements.txt
   ```

3. Put `PTX_ID` and `PTX_KEY` to `bustw_server/config.py`.
   ```bash
   vim bustw_server/config.py
   ```

4. Run it.
   ```bash
   python3 run.py
   ```

   Or run by `gunicorn`.
   ```bash
   pip3 install gunicorn
   gunicorn -w 1 -k gthread --thread=8 run:app
   ```

Or run by `Docker`.
```bash
docker run --name bustw_server \
           --restart=always \
           -p 65432:8000 -d \
           -e DOMAIN='bus.ntut.com.tw' \
           -e PTX_ID='[hidden]' \
           -e PTX_KEY='[hidden]' \
           pinlin/bustw_server
```

## License
MIT License

## Source
[![公共運輸整合資訊流通服務平臺（Public Transport data eXchange, PTX）](https://imgur.com/wp2gOeU.png)](http://ptx.transportdata.tw/PTX)
