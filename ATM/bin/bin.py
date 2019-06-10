# __author__:Lenovo  "Yang Tian"
# date:2018/7/28
import sys, os, json

# print(sys.path.append('F:\\Python Project\\ATM'))  #None
# print(__file__)  #F:/Python Project/ATM/bin/bin.py   在控制台中输出是:bin.py  即相对目录
# print(os.path.abspath(__file__)) #F:\Python Project\ATM\bin\bin.py
# print(os.path.dirname(os.path.abspath(__file__)))  #F:\Python Project\ATM\bin
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 找到根路径  ATM
sys.path.append(BASE_DIR)

from module import main

# from module import main  #因为bin.py是在bin文件夹下面，所有无法直接找到module
# main.main()  # No module named 'logger'   当前路径在bin下，所以main里面使用import logger调用logger会报错

main.run()