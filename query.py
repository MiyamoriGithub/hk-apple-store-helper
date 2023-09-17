import requests
import json
import os
from datetime import datetime
import time
import urllib3
from loguru import logger


if __name__ == '__main__':
    urllib3.disable_warnings()
    logger.add('logs/available.log',
               level='INFO',
               format='{time:YYYY-MM-DD HH:mm:ss} - {message}',
               rotation="10 MB")

    headers = {
        'content-type': 'application/json;encoding=UTF8;charset=UTF-8',
        'Origin': 'https://www.apple.com',
        'Referer': 'https://www.apple.com/hk-zh/shop/buy-iphone/iphone-15-pro',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }
    session = requests.session()

    count = 0
    module = {
        'module': 'MTQA3ZA/A',
        'name': 'Pro原色256GB'
    }
    with open('config.json', 'r') as config_json:
        module = json.load(config_json)

    while True:
        try:
            number = module['module']
            name = module['name']
            fulfill_message = session.get('https://www.apple.com/hk-zh/shop/fulfillment-messages?pl=true&mts.0=regular&mts.1=compact&parts.0=' +
                                          number + '&location=香港', headers=headers, verify=False, timeout=10)
            fulfill_json = json.loads(fulfill_message.text)
            if fulfill_json['head']['status'] != '200':
                os.system('say "your program is error!"')
                break
            store_list = fulfill_json['body']['content']['pickupMessage']['stores']
            flag = False
            for store in store_list:
                if store['partsAvailability'][number]['pickupDisplay'] == 'available':
                    flag = True
                    location = store['storeName']
                    available_time = store['partsAvailability'][number]['pickupSearchQuote']
                    colon_index = str(available_time).index('：')
                    available_time = available_time[colon_index + 2:]
                    currentDateAndTime = datetime.now()
                    logger.info(location + '備妥於: ' + available_time)
                    os.system('say "available: ' +
                              location + available_time + '"')
                    break
            if not flag:
                currentDateAndTime = datetime.now()
                print(str(currentDateAndTime) + ':' + name + '無貨')
            time.sleep(5)
        except Exception:
            currentDateAndTime = datetime.now()
            print(str(currentDateAndTime) + ': timeout, retrying')
