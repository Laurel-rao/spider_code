# _*_ coding:utf-8 _*_
'''
Author: Laurel-rao
create time:2018/11/15 上午10:41
Remark: 获取用户信息
'''
import json
import re


def _input(info):
    return input(info).strip().upper()


def get_user_info():
    '''
        获取乘客信息
    :return:
    '''
    name = _input("请输入姓名: ")

    while True:
        idcard = _input("请输入身份证号码: ")
        rex = "^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$"
        if not re.match(rex,idcard):
            print("身份证号码格式错误")
            continue
        else:
            break

    while True:
        phone = _input("请输入手机号码: ")
        if not re.match("^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\d{8}$", phone):
            print("手机号码格式错误")
            continue
        else:
            break
    data = {"name": name,
            "idcard": idcard,
            "phone": phone}
    data.update(get_train_times())
    with open("./conf/info.json", 'w') as ff:

        json.dump(data, ff, indent=2)


def get_train_times():
    '''
        获取车次信息
    :return:
    '''
    while True:
        _time = _input("请输入出发时间（2018-11-11）: ")
        if re.match("^\d{4}-(0\d|1[0-2])-([0-2][1-9]|3[01])$", _time):
            break
        else:
            print("日期输入错误")

    with open("./conf/city_code.json", 'r') as load_f:
        load_dict = json.load(load_f)

    def get_code(word):
        for i in load_dict:
            if i['name'] == word:
                return i
    while True:
        _start = _input("请输入出发城市: ")
        _end = _input("请输入到达城市: ")
        start = get_code(_start)
        end = get_code(_end)

        if not (start and end):
            print(start, "---", end)
            print("车站查询错误")
        else:
            break

    _train_times = _input("请输入车次: ")

    name = re.compile("(\d|k|t|z|d|g|n|a|y|x)", flags=re.IGNORECASE)
    if not name.match(_train_times):
        print("车次输入错误，请重新输入")
        _train_times = _input("请输入车次: ").strip()
    level = re.compile("(d|g)", flags=re.IGNORECASE)
    if level.match(_train_times):
        while True:
            seat_level = _input("请输入要哪种座位，一等座请输入M, 二等座请输入O, 商务座请输入9, 动卧请输入F, 高级软卧请输入A: ")
            if seat_level == "M":
                while True:
                    choose_seats = _input("请输入座位-(A|B|C|D|F):")
                    if choose_seats in ["A", "B", "C", "D", "F"]:
                        break
                    else:
                        print("选择错误，请重新选择")
            elif seat_level == "O":
                while True:
                    choose_seats = _input("请输入座位-(A|C|D|F):")
                    if choose_seats in ["A", "C", "D", "F"]:
                        break
                    else:
                        print("选择错误，请重新选择")
            elif seat_level == "9":
                while True:
                    choose_seats = _input("请输入座位-(A|C|F):")
                    if choose_seats in ["A", "C", "F"]:
                        break
                    else:
                        print("选择错误，请重新选择")
            elif seat_level in ["A", "F"]:
                choose_seats = None
            else:
                print("座位输入错误, 请重新输入")
                continue
            choose_seats = "1" + choose_seats if choose_seats else choose_seats
            break
    else:
        choose_seats = None
        while True:
            seat_level = _input("请输入要哪种座位, 硬座/无座请输入1, 硬卧请输入3, 软卧请输入4:")
            if seat_level in ["1", "3", "4"]:
                break
            else:
                print("座位输入错误，请重新输入")

    data = {"_time": _time,
            "_train_times": _train_times,
            "start": start, "end": end,
            "seat_level": seat_level,
            "choose_seats": choose_seats}
    return data