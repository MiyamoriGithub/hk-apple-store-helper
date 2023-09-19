import requests
import json
import os
from datetime import datetime
import time
import urllib3
from loguru import logger


class HkAppleStoreHelper:

    def __init__(self) -> None:
        urllib3.disable_warnings()
        self.module = {
            'module': 'MTQA3ZA/A',
            'name': 'Pro原色256GB'
        }
        with open('config.json', 'r') as config_json:
            config = json.load(config_json)
            self.module = config['module']
            self.log_enabled = config['logEnabled']
            self.bark_enabled = config['notification']['bark']['barkEnabled']
            self.bark_url = config['notification']['bark']['barkUrl']
            self.voice_enabled = config['notification']['voiceEnabled']
        if self.log_enabled:
            logger.add('logs/available.log',
                       level='INFO',
                       format='{time:YYYY-MM-DD HH:mm:ss} - {message}',
                       rotation="10 MB")
        if self.bark_enabled:
            self.bark_session = requests.session()
        self.session = requests.session()
        self.headers = {
            'content-type': 'application/json;encoding=UTF8;charset=UTF-8',
            'Origin': 'https://www.apple.com',
            'Referer': 'https://www.apple.com/hk-zh/shop/buy-iphone/iphone-15-pro',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        }

    def query_stock(self) -> None:
        module = self.module
        session = self.session
        headers = self.headers
        try:
            number = module['module']
            name = module['name']
            fulfill_message = session.get('https://www.apple.com/hk-zh/shop/fulfillment-messages?pl=true&mts.0=regular&mts.1=compact&parts.0=' +
                                          number + '&location=香港', headers=headers, verify=False, timeout=10)
            fulfill_json = json.loads(fulfill_message.text)
            if fulfill_json['head']['status'] != '200':
                os.system('say "your program is error!"')
                return
            store_list = fulfill_json['body']['content']['pickupMessage']['stores']
            flag = False
            for store in store_list:
                if store['partsAvailability'][number]['pickupDisplay'] == 'available':
                    flag = True
                    self.__notification_and_log(store, module)
                    break
            if not flag:
                currentDateAndTime = datetime.now()
                print(str(currentDateAndTime) + ':' + name + '無貨')
            time.sleep(5)
        except Exception:
            currentDateAndTime = datetime.now()
            print(str(currentDateAndTime) + ': timeout, retrying')

    def __notification_and_log(self, store, module) -> None:
        location = store['storeName']
        number = module['module']
        name = module['name']
        available_time = store['partsAvailability'][number]['pickupSearchQuote']
        colon_index = str(available_time).index('：')
        available_time = available_time[colon_index + 2:]
        if self.log_enabled:
            logger.info(location + '備妥於: ' + available_time)
        if self.bark_enabled:
            self.__bark_notification(name, location, available_time)
        if self.voice_enabled:
            self.__voice_notification(location, available_time)

    def __bark_notification(self, name: str, location: str, available_time: str) -> None:
        text = '{} {}備妥於Apple Store：{}'.format(
            available_time, name, location)
        headers = {
            'Content-Type': 'application/json;encoding=UTF8;charset=UTF-8'
        }
        body = {
            'title': 'iPhone已備妥',
            'body': text
        }
        resp = self.bark_session.post(
            self.bark_url, headers=headers, json=body, verify=False)
        text = resp

    def __voice_notification(self, location: str, available_time: str) -> None:
        os.system('say "available: ' + location + available_time + '"')


if __name__ == '__main__':
    helper = HkAppleStoreHelper()

    while True:
        helper.query_stock()
