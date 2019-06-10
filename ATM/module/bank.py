#__author__:Lenovo  "Yang Tian"
#date:2018/7/29
import json, time
from logger import logger

# login_status = False

def interactive_bank(card_info_my, card_info):
    menu_bank = u'''
    - - - - - - - - Choose Bank Option - - - - - - - -\033[33;1m
    1.  账户信息
    2.  还款
    3.  取款
    4.  转账
    5.  账单
    6.  退出
    \033[0m'''
    menu_bank_dic = {
        '1':account_info,
        '2':repay,
        '3':withdraw,
        '4':transfer,
        '5':pay_check,
        '6':logout
    }
    exit_flag = False
    while not exit_flag:
        print(menu_bank)
        choice = input('>>:').strip()
        if choice in menu_bank_dic:
            result = menu_bank_dic[choice](card_info_my, card_info)
            if choice == '6':
                exit_flag = True
            else:
                card_info_my = result[0]
                card_info = result[1]
        else:
            print("\033[31;1mOption does not exist!\033[0m")

def login_bank():
    # global login_status
    # if login_status:
    #     return True
    login_count = 0
    while login_count < 3:
        card_number = input('input card number>>>:')
        password = input('input card password>>>:')
        if not card_number.isdigit():
            print('卡号为纯数字！')
            continue
        card_number = int(card_number)
        with open(r'../conf/bank_account', 'r', encoding='utf-8') as f_read:
            data = json.load(f_read)
            for card_info in data:
                if card_info['card'] == card_number and card_info['password'] == password:
                    login_status = True
                    return True, card_info, data
            else:
                print('账号密码错误！')
        login_count += 1
    else:
        print("您只有三次机会！")
        return False, None

def quota(card_info):
    return card_info['quota']

def balance(card_info):
    return card_info['balance']

def add_pay_check(card_info_my, content):
    time_format = '%Y-%m-%d %X'
    time_current = time.strftime(time_format)
    if 'pay_check' in card_info_my:
        card_info_my['pay_check'] += time_current +  "  " +content
    else:
        card_info_my['pay_check'] = time_current +  "  " + content
    return card_info_my

def check(card_info, spend):  # 结账
    if balance(card_info) + quota(card_info) < spend:
        return False,card_info
    if balance(card_info) >= spend:
        card_info['balance'] -= spend
    else:
        card_info['quota'] = card_info['balance'] + card_info['quota'] - spend
        card_info['balance'] = 0
        time_format = '%Y-%m-%d %X'
        time_current = time.strftime(time_format)  #借款日期
        if 'time' not in card_info:
            card_info['time'] = time_current
    card_info = add_pay_check(card_info,'您购买商品消费%s，当前余额为%s,额度为%s\n' %(spend, balance(card_info), quota(card_info)))
    return True,card_info

def account_info(card_info_my, card_info):#卡信息
    print(card_info_my)
    return card_info_my, card_info

def repay(card_info_my, card_info):  #还款
    # time_lend = '2018-07-30 15:03:54'
    time_format = '%Y-%m-%d %X'
    time_current = time.strftime(time_format)
    if 'lend_time' in card_info_my:
        time_lend = card_info_my['lend_time']
        month_lend = int(time_lend[5:7])
        day_lend = int(time_lend[8:10])
        month_now = int(time_current[5:7])
        day_now = int(time_current[8:10])
        if month_lend == month_now or (month_lend + 1 == month_now and day_lend >= day_now):
            print('您于%s欠款%s,请于一个月内归还！' %(time_lend, 15000 - card_info_my['quota']))
        else:
            print('过期未还！')
    else:
        print('您尚不欠款！')
    card_index = card_info.index(card_info_my)
    back_flag = False
    while not back_flag:
        repay_amount = input('请输入还款金额：').strip()
        if repay_amount.isdigit():
            repay_amount = int(repay_amount)
            if 15000 - card_info_my['quota'] < 0:
                if repay_amount + card_info_my['quota'] > 15000:
                    card_info_my['balance'] = repay_amount + card_info_my['quota'] - 15000
                    card_info_my['quota'] = 15000
                else:
                    card_info_my['quota'] += repay_amount
            else:
                card_info_my['balance'] += repay_amount
            string = '您存款%s,当前余额为%s,额度为%s\n' %(repay_amount,card_info_my['balance'],card_info_my['quota'])
            print(string)
            card_info_my = add_pay_check(card_info_my,string)
            logger.logging_bank(str(card_info_my['card']) + string[1:])
            card_info[card_index] = card_info_my
            back_flag = True
        else:
            print('请输入数字！')
    return card_info_my,card_info

def withdraw(card_info_my, card_info): #提现
    card_index = card_info.index(card_info_my)
    back_flag = False
    while not back_flag:
        amount = input('请输入提现金额:')
        if not amount.isdigit():
            print('金额格式输入错误！')
            break
        amount = int(amount)
        if card_info_my['balance'] >= amount * 1.05:
            card_info_my['balance'] -= amount * 1.05
            string = '您成功提现%s, 收取手续费%s, 当前余额为%s\n' %(amount, amount * 0.05, card_info_my['balance'])
            print(string)
            # logger.logging_bank('%s提现%s, 收取手续费%s, 当前余额为%s' %(card_info_my['card'],amount, amount * 0.05, card_info_my['balance']))
            card_info_my = add_pay_check(card_info_my,string)
            logger.logging_bank(str(card_info_my['card']) + string[1:])
            card_info[card_index] = card_info_my
            back_flag = True
        else:
            print('当前余额不足')
    return card_info_my,card_info

def transfer(card_info_my,card_info): #转账
    back_flag = False
    while not back_flag:
        card_number = input('请输入对方卡号:')
        if not card_number.isdigit():
            print('卡号为纯数字')
            continue
        else:
            card_number = int(card_number)
            for card_info_he in card_info:
                if card_info_he['card'] == card_number:
                    choice = input('请确认对方卡号(y/n):')
                    if choice == 'y' or choice == 'Y':
                        while True:
                            amount = input('请输入转账金额:')
                            if not amount.isdigit():
                                print('您输入的金额格式错误！')
                                continue
                            else:
                                final_choice = input('确认转账？(y/n):')
                                if final_choice == 'y' or final_choice == 'Y':
                                    amount = int(amount)
                                    if balance(card_info_my) >= amount:
                                        card_index_my = card_info.index(card_info_my)
                                        card_index_his = card_info.index(card_info_he)
                                        card_info_my['balance'] -= amount
                                        card_info_he['balance'] += amount

                                        print('您成功给%s转账%s,当前余额为%s' % (card_number,amount, card_info_my['balance']))
                                        logger.logging_bank('%s成功给%s转账%s,当前余额为%s' % (card_info_my['card'],card_number,amount, card_info_my['balance']))
                                        card_info_my = add_pay_check(card_info_my, '您成功给%s转账%s,当前余额为%s\n' % (card_number,amount, card_info_my['balance']))
                                        card_info_he = add_pay_check(card_info_he, '%s成功给您转账%s,当前余额为%s\n' % (card_info_he['card'], amount, card_info_he['balance']))
                                        card_info[card_index_my] = card_info_my
                                        card_info[card_index_his] = card_info_he
                                    else:
                                        print('您当前余额为%s,无法转账%s到其他用户' % (card_info_my['balance'], amount))
                                    back_flag = True
                                    break
                                elif final_choice == 'n' or final_choice == 'N':
                                    continue
                                else:
                                    print('输入错误，请重新输入！')
                    elif choice == 'n' or choice == 'N':
                        break
                    else:
                        print('输入错误，请重新输入！')
                        break
            else:
                if not back_flag:
                    print('对方卡号不存在！')
    return card_info_my,card_info

def pay_check(card_info_my, card_info):
    if 'pay_check' in card_info_my:
        print(card_info_my['pay_check'])
    else:
        print('您当前还没有消费记录')
    return card_info_my,card_info

def logout(card_info_my, card_info):
    with open(r'..\conf\bank_account', 'w', encoding='utf-8') as f:
        json.dump(card_info,f,ensure_ascii=False)
    print('成功退出登录！')
    return

def run():
    info = login_bank()
    if True in info:
        card_info_my = info[1]
        card_info = info[2]
        print(card_info_my)
        print(card_info)
        interactive_bank(card_info_my, card_info)




if __name__ == '__main__':
    card_info = login_bank()
    print(card_info)
    if True in card_info:
        # print(balance(card_info[1]))
        # print(quota(card_info[1]))
        # trans_money(card_info[1])
        # withdraw(card_info[1])
        # repay(card_info[1])
        run()
