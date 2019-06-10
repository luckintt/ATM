#__author__:Lenovo  "Yang Tian"
#date:2018/7/28
from logger import  logger
from module import  bank, user

def exit_pro():
    print('Finish the operation in this level!')
    return True

# def bank():
#     bank.run()
#
# def user():
#     user.run()

def interactive_top():
    menu_top = u'''
            - - - - - - - - Choose Option - - - - - - - -\033[32;1m
            1.  银行操作
            2.  购物车操作
            3.  退出
            \033[0m'''
    menu_top_dic = {
        '1': bank.run,
        '2': user.run,
        '3': exit_pro,
    }
    exit_flag = False
    while not exit_flag:
        print(menu_top)
        choice = input('>>:').strip()
        if choice in menu_top_dic:
            menu_top_dic[choice]()
            if choice == '3':
                exit_flag = True
        else:
            print("\033[31;1mOption does not exist!\033[0m")


def run():
    interactive_top()
