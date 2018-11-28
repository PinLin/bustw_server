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

   or Run by `gunicorn`.
   ```bash
   pip3 install gunicorn gevent
   gunicorn -w 1 -k gevent run:app
   ```

## Source
[![公共運輸整合資訊流通服務平臺（Public Transport data eXchange, PTX）](https://imgur.com/wp2gOeU.png)](http://ptx.transportdata.tw/PTX)