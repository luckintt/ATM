#__author__:Lenovo  "Yang Tian"
#date:2018/7/28
import time, json
def logging_shop(content):
    time_format = '%Y-%m-%d %X'
    time_current = time.strftime(time_format)
    # print(time_current)
    with open('购物日志记录', 'a', encoding='utf-8') as f:
        # json.dump('%s end action %s\n' % (time_current, content), f, ensure_ascii=False)
        f.write('%s  %s  end action\n' % (time_current, content))

def logging_bank(content):
    time_format = '%Y-%m-%d %X'
    time_current = time.strftime(time_format)
    # print(time_current)
    with open('ATM操作日志', 'a', encoding='utf-8') as f:
        # json.dump('%s end action %s\n' % (time_current, content), f, ensure_ascii=False)
        f.write('%s  %s  end action\n' % (time_current, content))



