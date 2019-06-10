#__author__:Lenovo  "Yang Tian"
#date:2018/7/29

import os, json
from conf import settings
from module import bank
from logger import logger

def interactive_cart(user_info):
    if len(user_info[1]) == 3:
        buy = {}  # 用于记录用户已经购买的商品
        # salary = input('salary:')
        # while not salary.isdigit():
        #     print('工资格式输入错误！')
        #     salary = input('salary>>>:')
        # salary = float(salary)
    else:
        buy = user_info[1][3]
        # salary = user_info[1][3]
        # print('\033[1;43;43m',end='')
        # print('您剩余工资为%s' %salary,end='')
        # print('\033[0m')
    card_info_all = []
    while True:
        i = 0
        print('所有商品信息如下'.center(50, '*'))
        print('\033[31;1m',end='')
        while i < len(settings.goods):
            print('%s.\t%s\t%s' % (i, settings.goods[i]['name'], settings.goods[i]['price']))
            i += 1
        print('\033[0m',end='')

        choice = input('[退出:q] [查询记录:s] 输入商品序号>>>:').strip()
        if choice.isdigit():
            choice = int(choice)
            if choice >= 0 and choice < len(settings.goods):
                while True:
                    card_info = bank.login_bank()  # 输入卡号和密码
                    if True in card_info:
                        check_result = bank.check(card_info[1], settings.goods[choice]['price'])  # 结账
                        print(check_result)
                        if True in check_result:
                            card_info[2][card_info[2].index(card_info[1])] = check_result[1]
                            card_info[1]['quota'] = check_result[1]['quota']  # 更正卡信息
                            card_info[1]['balance'] = check_result[1]['balance']
                            card_info_all = card_info[2]
                            print(card_info_all)

                            thing_name = settings.goods[choice]['name']
                            print('\033[1;43;43m', end='')
                            print('您已成功购买%s,消费了%s, 剩余余额为%s, 剩余额度为%s' % (settings.goods[choice]['name'],
                                                                        settings.goods[choice]['price'],
                                                                        card_info[1]['balance'], card_info[1]['quota']),
                                  end='')
                            print('\033[0m')
                            if thing_name not in buy:  # 用户没买过该商品
                                buy[thing_name] = [settings.goods[choice]['price'], 1, settings.goods[choice]['price']]
                            else:
                                buy[thing_name][1] += 1
                                buy[thing_name][2] = buy[thing_name][0] * buy[thing_name][1]  # 小计 = 单价 * 数量
                            logger.logging_shop(
                                '%s购买%s消费了%s, 剩余余额为%s' % (user_info[1][0], settings.goods[choice]['name'],
                                                          settings.goods[choice]['price'], card_info[1]['balance']))
                            logger.logging_bank(
                                '%s消费了%s, 剩余余额为%s, 剩余额度为%s' % (card_info[1]['card'], settings.goods[choice]['price'],
                                                               card_info[1]['balance'], card_info[1]['quota']))
                            break
                        else:
                            print('\033[1;43;43m', end='')
                            print('您的余额为%s,额度为%s,不足以购买此商品。' % (card_info[1]['balance'], card_info[1]['quota']), end='')
                            print('\033[0m')
                            break
                    else:
                        op = input('账号密码错误！是否重新输入？(y/n):')
                        if op == 'y' or op == 'Y':
                            continue
                        else:
                            break
            else:
                print('该商品不存在')
        elif choice == 'q' or choice == 's':
            if buy:
                print('您购买了如下商品'.center(50, '*'))
                print('商品名\t单价\t数量\t小计')
                for i in buy:
                    print('%s\t%s\t\t%s\t\t%s' % (i, buy[i][0], buy[i][1], buy[i][2]))
            else:
                print('您还没有购买商品')

            if choice == 'q':
                if len(user_info[1]) == 3:  # 该用户之前没有买东西
                    user_info[2].index(user_info[1]).append(buy)
                else:
                    user_index = user_info[2].index(user_info[1])
                    user_info[2][user_index][3].update(buy)
                    with open(r'../conf/user_account', 'w', encoding='utf-8') as f_write:
                        json.dump(user_info[2], f_write, ensure_ascii=False)
                    with open(r'../conf/bank_account', 'w', encoding='utf-8') as f_write:
                        json.dump(card_info_all, f_write, ensure_ascii=False)
                return
        else:
            print('输入错误！')


def login_cart():  #检测登录是否成功
    account = []  # 利用列表account来存储所有用户的信息
    with open(r'../conf/user_account', 'r', encoding='utf8') as f_read:
        account = json.load(f_read)

    count_unvaild = 0  # 输入的用户名无效次数
    dic_valid = {}  # 用户统计每个注册后的用户名输入错误次数
    while count_unvaild < 3:
        username_exit = False  # 标志用户名是否存在
        username = input("username>>>:")
        for user_info in account:
            if username in user_info:
                username_exit = True
                if user_info[2]:  # 若用户名存在，且该用户被锁定
                    print('Your account have been locked!')
                    return False, None
                else:
                    password = input("password>>>:")
                    if password == user_info[1]:  # 用户名密码正确
                        print("Welcome %s login...." % username)
                        return True, user_info, account
                    else:  # 密码错误
                        print("Your password is wrong!")
                if username not in dic_valid:  # 统计每次输入的用户名总共的输入次数
                    dic_valid[username] = 1
                else:
                    dic_valid[username] += 1
                if dic_valid[username] == 3:  # 被锁定的用户一定是最后一次输入的用户，因为之前输入的用户名若错误了三次，经过这个判断时会被锁定
                    user_info[2] = 1  # 修改列表中该用户的锁定信息
                    print('Password error for three times，and your account will be locked!')

                    with open('Account', 'w', encoding='utf8') as f_write:
                        json.dump(account, f_write, ensure_ascii=False)
                    return False, None
        if not username_exit:  # 若用户名不存在，则输出对应提示信息
            print("Username is not exist")
            count_unvaild += 1
    else:  # 当用户输入不存在的用户名达到三次时执行
        print('Username error for three times!')
        return False, None


def run():
    user_info = login_cart()
    if True in user_info:  # 用户成功登录
        interactive_cart(user_info)


