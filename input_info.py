# _*_ coding:utf-8 _*_
'''
Author: Laurel-rao
create time:2018/11/15 上午10:41
Remark: 获取用户信息
'''
import json
import re


def get_user_info():
    '''
        获取乘客信息
    :return:
    '''
    while True:
        name = input("请输入姓名: ").strip()
        idcard = input("请输入身份证号码: ").strip()
        phone = input("请输入手机号码: ").strip()
        seat_level = input("请输入要哪种座位，一等座请输入M, 二等座请输入o, 商务座请输入9, 硬座请输入1, 硬卧请输入3, 软卧请输入4:  ")
        if not re.match("^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$",
                        idcard):
            print("身份证号码格式错误")
            continue
        if not re.match("^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\d{8}$", phone):
            print("手机号码格式错误")
            continue
        return [seat_level, name, idcard, phone]
        # 获取预售时间

def get_train_times():
    '''
        获取车次信息
    :return:
    '''
    _time = input("请输入出发时间: ").strip()

    _train_times = input("请输入车次: ").strip()
    _start = input("请输入出发车站名: ").strip()
    _end = input("请输入终点车站名: ").strip()
    with open("./conf/city_code.json", 'r') as load_f:
        load_dict = json.load(load_f)

    def get_code(word):
        for i in load_dict:
            if i['name'] == word:
                return i

    start = get_code(_start)
    end = get_code(_end)

    if not (start and end):
        print(start, "---", end)
        print("车站查询错误")
    else:
        print(start, end)
    return _time, _train_times, start, end