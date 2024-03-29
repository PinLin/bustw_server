# bustw_server
bus tracker for Taiwanese Server

## Usage
1. Clone.
   ```bash
   git clone https://github.com/PinLin/bustw_server
   cd bustw_server
   ```

2. Install dependencies.
   ```bash
   portry install
   ```

3. Put `PTX_ID` and `PTX_KEY` to `bustw_server/config.py`.

4. Run it.
   ```bash
   poetry run python3 app.py
   ```

   Or run by `gunicorn`.
   ```bash
   pip3 install gunicorn
   gunicorn -w 1 -k gthread --thread=8 app:app
   ```

Or run by `Docker`.
```bash
docker run --name bustw_server \
           --restart=always \
           -p 8000:8000 -d \
           -e PTX_ID='<PTX_ID>' \
           -e PTX_KEY='<PTX_KEY>' \
           pinlin/bustw_server
```

## License
[MIT](License)

## Source
[![公共運輸整合資訊流通服務平臺（Public Transport data eXchange, PTX）](https://imgur.com/wp2gOeU.png)](http://ptx.transportdata.tw/PTX)
