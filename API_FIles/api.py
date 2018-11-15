




#  2. 提交用户信息数据，初次提交订单
url = "https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo"

# '具体api'
js_url = 'https://kyfw.12306.cn/otn/resources/merged/queryLeftTicket_js.js?scriptVersion=1.9108'


passengerTicketStr = '座位编号, 未知, ticket_type, 饶佳俊, 身份证选1,362531199611254832,13694846652,N'

passenger_type = {
        "adult": "1",
        "child": "2",
        "student": "3",
        "disability": "4"
    },

ticket_type = {"1": "成人票",
                "2": "孩票",
                "3": "学生票",
                "4": "伤残军人票"}

seat_level = {
    "M": "一等座",
    "o": "二等座",
    '9': "商务座",
    '1': "硬座",
    '2': "无座",
    '3': "硬卧",
    "4": "软卧",
}
