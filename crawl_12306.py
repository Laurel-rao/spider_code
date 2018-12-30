# _*_ coding:utf-8 _*_
'''
Author: Laurel-rao
create time:2018/11/12 下午6:54
Remark: 
'''
import pickle
import json
import time

import requests
from common import *
from input_info import *

headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5)\ AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    "Host": "kyfw.12306.cn",
    "origin": "https://kyfw.12306.cn",
}


def check_users(req=None, cookie={}):
    '''
        确认用户在登录状态
    :return:
    '''
    with open('./conf/cookie.json', "r") as fff:
        cookie = json.load(fff)

    url = 'https://kyfw.12306.cn/otn/login/checkUser'
    if not req:
        req = requests.session()
    rep = req.post(url, headers=headers, data={"_json_att": ""}, cookies=cookie)
    if rep.status_code == 200:
        try:
            if rep.json().get("data").get("flag"):
                return req
            print(rep.json().get("data").get("flag"))
        except:
            print(rep.text)
    return False


def check_login():
    if not check_users():
        req = login()
    else:
        req = requests
    return req


def login():
    # 1. 获取登录二维码
    req = requests.session()
    req.get('https://www.12306.cn/index/')
    response = req.post('https://kyfw.12306.cn/otn/login/conf', headers=headers)
    if response.status_code != 200:
        print("网络异常请求错误")
    url = 'https://kyfw.12306.cn/passport/web/create-qr64'

    # 1.1 打开图片,并获取 uuid
    req, uuid = open_image(req, url)

    # 1.2 扫描二维码，并获取 umatk  初级秘钥
    n = 0
    start = time.perf_counter()
    while True:
        url1 = 'https://kyfw.12306.cn/passport/web/checkqr'
        param = {'uuid': uuid, 'appid': 'otn'}
        time.sleep(1)
        response = req.post(url1, data=param)
        m = n % 6
        print("\r正在检查是否登录%s" % (m * "."), end='')
        n += 1

        if response.status_code == 200 and eval(response.text).get('result_code') == '1':
            # 扫描成功，请确认
            # print("扫描成功，请确认")
            pass
        elif response.status_code == 200 and eval(response.text).get('result_code') == '2':
            # 登录成功
            break
        elif response.status_code == 200 and eval(response.text).get('result_code') == '3':
            # 五分钟过期
            end = time.perf_counter()
            print(end - start)
            print("二维码已失效, 正在重新获取")
            req, uuid = open_image(req, url)
        else:
            pass

    # 2. 使用秘钥登录验证

    login_url1 = 'https://kyfw.12306.cn/passport/web/auth/uamtk'  # 2.1 将登录的初始秘钥发送，获取二级秘钥
    login_url2 = 'https://kyfw.12306.cn/otn/uamauthclient'  # 2.2 将二级秘钥发送至服务器确认，确认后生效
    login_url3 = 'https://kyfw.12306.cn/otn/login/conf'  # 2.3 确认二级密钥已生效
    rep1 = req.post(login_url1, headers=headers, data={'appid': 'otn'})
    uamtk = rep1.json().get("newapptk")
    req.post(login_url2, headers=headers, data={'tk': uamtk})
    req.post(login_url3, headers=headers)
    cookie = req.cookies.get_dict()
    del cookie['uamtk']
    write_cookie(cookie)

    # 3. 验证是否登录
    if check_users(req):
        print("登陆成功")
        try:
            save_obj(req)
        except:
            print('save_obj error')
        return req
    else:
        print("登陆失败")
        return False


def get_ticket():
    info = get_info()
    url = "https://kyfw.12306.cn/otn/leftTicket/queryZ"
    params = {'leftTicketDTO.train_date': info['_time'], 'leftTicketDTO.from_station': "%s" % (info['start']['code']), \
              "leftTicketDTO.to_station": "%s" % (info['end']['code']), "purpose_codes": "ADULT"}
    rep = requests.get(url, params=params)
    cookie = rep.cookies.get_dict()
    write_cookie(cookie)
    if rep.status_code != 200:
        print('ticket query 网络异常')

    result = rep.json().get("data").get("result")
    for i in result:
        if re.search(info['_train_times'], i.upper()):
            return i
    else:
        return "查询错误，无该车次"


def is_login():
    start = time.perf_counter()
    n = 0
    req = check_login()
    while True:
        time.sleep(1)
        m = n % 6
        print("\r正在检查是否登录%s" % (m * "."), end='')
        n += 1
        if not check_users(req):
            break


    end = time.perf_counter()
    print("\ncookie 存活时间为:%s" % (end - start))


def first_submit(req, res_dict):
    url = "https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest"
    info = get_info()
    data = {
        'secretStr': res_dict['secret'],
        'train_date': info['_time'],  # 单程出发日
        'back_train_date': '2018-11-29',  # 返程出发日
        'tour_flag': 'dc',  # 单程 、 往返(wf)
        'purpose_codes': 'ADULT',  # 成人，学生(STUDENT)
        'query_from_station_name': info['start']['name'],
        'query_to_station_name': info['end']['name'],
        'undefined': ''
    }
    for i in data:
        print("%s : %s"%(i, data[i]))
    rep = req.post(url, data=data, headers=headers)
    if rep.status_code != 200:
        print('3. first_submit 网络异常')

    # 三种情况， 1. tk错误，返回一个网页， 2. serectstr错误， 返回json，flag=False, 3. 请求成功
    try:
        data = rep.json().get('status')
    except:
        data = None
    if data:
        print('3. first_submit:', rep.json())
        print('3. first_submit 请求成功')
    else:
        print(rep.text[:1000])
        print('3. first_submit 请求失败')
        return
    req, token, check = get_repeat_token(req)
    if not token:
        return

    pas_url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
    rep1 = req.post(pas_url, data={'REPEAT_SUBMIT_TOKEN': token, '_json_att': ''})

    try:
        _bool = rep1.json().get("status")
        if _bool:
            print("getPassengerDTOs 请求成功")
    except:
        print("getPassengerDTOs 请求失败")
    return req, token, check


def book_order(check_data, get_data, req, check):
    info = get_info()
    confirm_data = {
        "passengerTicketStr": check_data['passengerTicketStr'],
        'oldPassengerStr': check_data['oldPassengerStr'],
        'randCode': '',
        'purpose_codes': '00',
        'key_check_isChange': check,
        'leftTicketStr': get_data['leftTicket'],
        'train_location': get_data['train_location'],
        'choose_seatss': info['choose_seats'],
        'seatDetailType': '000',
        'whatsSelect': '1',
        'roomType': '00',
        'dwAll': 'N',
        '_json_att': '',
        'REPEAT_SUBMIT_TOKEN': check_data['REPEAT_SUBMIT_TOKEN'],
    }
    confirm_url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
    rep1 = req.post(confirm_url, data=confirm_data)
    if rep1.json().get('data').get("submitStatus"):
        print("购票成功")


def pay_for():
    pass


def get_repeat_token(req):
    url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
    rep = req.post(url)
    if rep.status_code != 200:
        print("get_repeat_token 网络错误")
    result = re.search("globalRepeatSubmitToken[\s\S]*?'(?P<token>[\s\S]+?)';", rep.text)
    res1 = re.search("key_check_isChange[\s\S]*?:'(?P<token>[\s\S]+?)','leftDetails'", rep.text)
    if not result:
        print("正则表达式1匹配错误")
        return
    if not res1:
        print("正则表达式2匹配错误")
        return

    return req, result.group("token"), res1.group("token")


def confirm_order(req, token, res_dict):
    check_url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
    get_url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
    info = get_info()
    check_data = {
        'cancel_flag': '2',
        'bed_level_order_num': '000000000000000000000000000000',
        # 'passengerTicketStr': 'O, 0, 1, 饶佳俊, 1, 362531199611254832, 13694846652, N',
        'passengerTicketStr': '%s,0,1,%s,1,%s,%s,N' % (info['seat_level'], info['name'], info['idcard'], info['phone']),
        'oldPassengerStr': '%s,1,%s,1_' % (info['name'], info['idcard']),
        'tour_flag': 'dc',
        'randCode': '',
        'whatsSelect': '1',
        '_json_att': '',
        'REPEAT_SUBMIT_TOKEN': token
    }
    times = trans(info['_time'])
    get_data = {
        # 'train_date': 'Tue Nov 20 2018 00:00: 00 GMT + 0800(中国标准时间)',
        'train_date': '%s 00:00: 00 GMT + 0800(中国标准时间)' % times,
        'train_no': res_dict['train_no'],
        'stationTrainCode': res_dict['train_name'],
        'seatType': info['seat_level'],
        'fromStationTelecode': res_dict['_from'],
        'toStationTelecode': res_dict['_to'],
        'leftTicket': res_dict['left_ticket'],
        'purpose_codes': '00',
        'train_location': res_dict['train_location'],
        '_json_att': '',
        'REPEAT_SUBMIT_TOKEN': token,
    }
    #  该请求无法正常响应
    if not check_users(req):
        print("登录失败")
        return
    rep1 = req.post(check_url, data=check_data, headers=headers)
    # print(rep1.headers)
    try:
        data1 = rep1.json().get("data").get('submitStatus')
    except:
        data1 = ''
    if data1:
        print("checkOrderInfo 请求成功")

    else:
        print(rep1.text)
        print("checkOrderInfo 请求失败")

    rep2 = req.post(get_url, data=get_data, headers=headers)

    try:
        data2 = rep2.json().get("status")
    except:
        data2 = ''
    if data2:
        # print(rep2.json().get('data'))
        print("getQueueCount 请求成功")
    else:
        print(rep2.text[:1000])
        print("getQueueCount 请求失败")

    return check_data, get_data, req


def main():

    if not get_info():
        get_user_info()
    #  2. 登录
    cookie = get_cookie()
    req = check_users(cookie=cookie)
    if not req:
        req = login()  # 使用扫码登录

    # 查询车次，订单中有 serectStr， globalRepeatSubmitToken

    text = get_ticket()
    res_dict = parse_html(text)
    if not check_users():
        print("用户登录已失效")
        req = login()
    # secret, start_time, end_time, start_city, end_city = parse_params(res_dict, _time, _start, _end)
    # JSESSIONID  和  tk 正确, secretStr 正确， secret 需要解码，使用parse.quote 和 parse.unquote
    # 3. 提交初始订单
    while True:
        # 该请求成功后，其他请求失败概率较小
        submit_data = first_submit(req, res_dict)
        if submit_data:
            req, token, check = submit_data
            break
        else:
            print('first_submit 请求失败，正在重试')
            continue
    cookie = req.cookies.get_dict()
    check_data, get_data, req = confirm_order(req, token, res_dict)
    # 乘车人选择，确认订单，选择座位(高铁)
    # 下订单，并返回订单号
    book_order(check_data, get_data, req, check)


if __name__ == '__main__':
    main()


