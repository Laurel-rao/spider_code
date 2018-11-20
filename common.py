# _*_ coding:utf-8 _*_
'''
Author: Laurel-rao
create time:2018/11/15 上午10:17
Remark: 处理数据，文件
'''
import base64
import json
import pickle
import time
from urllib import parse

from PIL import Image

headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    "Host": "kyfw.12306.cn",
    "origin": "https://kyfw.12306.cn",
}


def trans(_time):
    '''
        转化时间
    :param _time: "2018-11-11"
    :return: "Nov Sun 11 2018"
    '''
    _t = time.strptime(_time, '%Y-%m-%d')
    return time.strftime("%b %a %d %Y", _t)


def write_cookie(cookie):
    '''
        将cookie写入文件
    :param cookie: dict-type
    :return: None
    '''
    with open("./conf/cookie.json", 'r') as f:
        _cookie = json.load(f)
    _cookie.update(cookie)
    with open("./conf/cookie.json", 'w') as ff:
        json.dump(_cookie, ff, indent=2)


def get_cookie():
    with open("./conf/cookie.json", 'r') as f:
        _cookie = json.load(f)
    return _cookie


def get_info():
    try:
        with open('./conf/info.json', 'r') as ff:
            info = json.load(ff)
    except:
        return None
    return info


def save_obj(req):
    with open("object.pkl", 'wb') as ff:
        pickle.dump(req, ff)


def get_obj():
    try:
        with open("object.pkl", 'rb') as ff:
            obj = pickle.load(ff)
    except:
        return False
    return obj


def open_image(req, url):
    '''
    get qr image
    :param url: url
    :return: request with session, uuid
    '''
    # req = requests.session()
    params = {"appid": "otn"}
    rep = req.post(url, headers=headers, data=params)
    try:
        rep.raise_for_status()
    except:
        print("请求失败")
        print(rep.url)
        print(rep.text)
    data = eval(rep.text)
    img = data.get('image')
    uuid = data.get("uuid")
    with open("./conf/qr_code.jpg", 'wb') as p:
        content = base64.b64decode(img)
        p.write(content)
    image = Image.open("./conf/qr_code.jpg")
    image.show()
    return req, uuid


def parse_params(res_dict, _time, _start, _end):
    '''
        处理用户输入数据
    :param res_dict: dict-type
    :param _time:  "2018-11-11"
    :param _start: '南昌'
    :param _end:  '深圳'
    :return: 处理完的数据
    '''
    secret = res_dict['secret']
    start_time = _time
    end_time = ''  # 返程时间未处理
    start_city = _start['name']
    end_city = _end['name']
    return secret, start_time, end_time, start_city, end_city


def parse_html(text):
    '''

    :param text: 处理查询到的车次数据
    :return:
    '''
    res = text.split("|")
    secret = parse.unquote(res[0])
    train_no = res[2]  # 车次编号
    train_name = res[3]  # 车次编号
    left_ticket = res[12]  # 车次编号
    train_location = res[15]
    _from = res[6]  # 出发地
    _to = res[7]  # 到达地

    ruanwo = res[23]  # 软卧
    yingwo = res[28]  # 硬卧
    yingzuo = res[29]  # 硬座
    erdengzuo = res[30]  # 二等座
    yidengzuo = res[31]  # 一等座
    wuzuo = res[26]  # 无座
    return {"secret": secret,
            "ruanwo": ruanwo,
            "train_no": train_no,
            "left_ticket": left_ticket,
            "train_location": train_location,
            "train_name": train_name,
            "_from": _from,
            "_to": _to,
            "yingwo": yingwo,
            "yingzuo": yingzuo,
            "erdengzuo": erdengzuo,
            "yidengzuo": yidengzuo,
            "wuzuo": wuzuo,
            }
