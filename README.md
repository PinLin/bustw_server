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

## License
MIT License

## Source
[![公共運輸整合資訊流通服務平臺（Public Transport data eXchange, PTX）](https://imgur.com/wp2gOeU.png)](http://ptx.transportdata.tw/PTX)
