#__author__:Lenovo  "Yang Tian"
#date:2018/7/28

import os,sys,json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  #找到根路径  ATM
sys.path.append(BASE_DIR)

goods = [
{"name": "电脑", "price": 1999},
{"name": "鼠标", "price": 10},
{"name": "游艇", "price": 20},
{"name": "美女", "price": 998}
]

# bank = [
# {'name':'alex', 'Card':11111111, 'password':'1111', 'quota':15000, 'balance':30000},
# {'name':'alvin', 'Card':22222222, 'password':'2222', 'quota':15000, 'balance':40000},
# {'name':'张三', 'Card':33333333, 'password':'3333', 'quota':15000, 'balance':30000}
# ]
#
# user = [
# ['alex', '123', 0, 10, {'电脑': [1999, 2, 3998], '鼠标': [10, 5, 50], '美女': [998, 1, 998], '游艇': [20, 2, 40]}],
# ['alvin', '123', 0, 8001.0, {'电脑': [1999, 1, 1999]}],
# ['张三', '333', 1],
# ]
#
# with open('bank_account', 'w', encoding='utf-8') as f_write:
#     json.dump(bank, f_write, ensure_ascii=False)
#
# with open('user_account', 'w', encoding='utf-8') as f_write:
#     json.dump(user, f_write, ensure_ascii=False)

