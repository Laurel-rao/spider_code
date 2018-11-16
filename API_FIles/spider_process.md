

# 爬虫主要流程

1. 登录模块
    
    1. 获取二维码 `https://kyfw.12306.cn/passport/web/create-qr64`
    2. 循环发送检测二维码api, 检测是否登录成功 `https://kyfw.12306.cn/passport/web/checkqr`
    3. 登录成功，退出检测循环 
    
2. 查询车次
    
    1. 参数获取车次信息 `https://kyfw.12306.cn/otn/leftTicket/init`
    2. 获取所有站台信息 `https://kyfw.12306.cn/otn/resources/js/framework/station_name.js`

3. 初次提交订单(车票未锁定)

    1. 初始信息提交  `https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest`
    2. 获取token，check `https://kyfw.12306.cn/otn/confirmPassenger/initDc`
    
```
        secretStr: RSa3yt9+mvFkGPWOrOQuDjb/ejfUTUmXEwv23lBJEn98/lspxjwQ8Gv8oMQIDc4jsVW+ZpdVuKal
        JUK9nMOacYjCPKGlLnFDzpwXU8QCPArHPKPsuSBeaJq54XPD3lRU/xVAnn3+jzT1PpjBdSOalRAW
        DUdPyYdb983bLGi2+rzB/7uOLtLyicoFzmNYgHWed5NvkVkrTjwnbs7EIn1PdBP/kE6HFrlbc93H
        /KYf2Y1zN5k+wTWbz7hlmQ+0AjSctC5p4R8CjTg=
        train_date: 2018-11-14       # 返程日
        back_train_date: 2018-11-13  # 出发日
        tour_flag: dc                # 单程 、 往返(wf)
        purpose_codes: ADULT         # 成人，学生(STUDENT)
        query_from_station_name: 南昌
        query_to_station_name: 深圳
        undefined:
    返回值:
        {'validateMessagesShowId': '_validatorMessage',
         'status': True,
         'httpstatus': 200,
         'data': 'Y',  # 当时间靠近时，是 Y， 当时间离得远时， 是 N
         'messages': [],
         'validateMessages': {}}

3.1 获取 token https://kyfw.12306.cn/otn/confirmPassenger/initDc
    post: _json_att:""
    返回值: html网页
```

4. 详细信息提交

    1. 确认乘客信息 `https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo`
    
```
    post:
        cancel_flag: 2
        bed_level_order_num: 000000000000000000000000000000

        # 此处可表示多张，最多买五张
        passengerTicketStr: 1,        0,   1,饶佳俊, 1,362531199611254832,13694846652,N
                            9 表示商务座     1. 成人票 居民身份证
                            o 表示二等座     2. 儿童票
                            M 表示一等座     3. 学生票
                            N_O            4. 残军票
                            表示不是一个选中的乘客，只能有一个O，有多个N_O，手机号码只选一个，使用空白代替 ,,
        oldPassengerStr: 饶佳俊,1,362531199611254832,1_
        tour_flag: dc
        randCode:
        whatsSelect: 1
        _json_att:
        REPEAT_SUBMIT_TOKEN: f611ff917f6ed7e6a214af4fdc285441

    返回值: submitStatus 为 True， 为确认成功
        # 绿皮车

        data: {checkSeatNum: true, errMsg: "您选择了1位乘车人，但本次列车硬座仅剩0张。", submitStatus: false}
        httpstatus: 200
        messages: []
        status: true
        validateMessages: {}
        validateMessagesShowId: "_validatorMessage"
        # 高铁

        data: {ifShowPassCode: "N", canChooseBeds: "N", canChooseSeats: "N", choose_seatss: "MOP9",…}
        httpstatus: 200
        messages: []
        status: true
        validateMessages: {}
        validateMessagesShowId: "_validatorMessage"
```

    2. 查询预定车次的车票信息 `https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount`

```
    post:
        train_date: Wed Nov 14 2018 00:00:00 GMT+0800 (中国标准时间)  发车日期，只需要改日期 wed nov 14 即可
        train_no: 5f00000K94B1   在query中可以查询
        stationTrainCode: K91
        seatType: 1
        fromStationTelecode: NCG
        toStationTelecode: BJQ
        leftTicket: XncsACvFq2raHyJQMkDHyEuAUM9zBu7NC228B%2BH1gLYbz3NJHkQmwTclqu8%3D
        purpose_codes: 00
        train_location: H6
        _json_att:
        REPEAT_SUBMIT_TOKEN: 2a372bbefb27888fe0d7513592a7a810

    返回信息
        data: {count: "0", ticket: "23,0", op_2: "false", countT: "0", op_1: "false"}
        httpstatus: 200
        messages: []
        status: true
        validateMessages: {}
        validateMessagesShowId: "_validatorMessage"
```


6. 提交订单 `https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue`

```
    post:
        passengerTicketStr: 1,0,1,饶佳俊,1,362531199611254832,13694846652,N
        oldPassengerStr: 饶佳俊,1,362531199611254832,1_
        randCode:
        purpose_codes: 00
        key_check_isChange: DDAA044DAD70A5113F323B1DB55F5B5703EFBCA3DE7B69190B78459B
        leftTicketStr: XncsACvFq2raHyJQMkDHyEuAUM9zBu7NC228B%2BH1gLYbz3NJHkQmwTclqu8%3D
        train_location: H6
        choose_seatss:
        seatDetailType: 000
        whatsSelect: 1
        roomType: 00
        dwAll: N
        _json_att:
        REPEAT_SUBMIT_TOKEN: 2a372bbefb27888fe0d7513592a7a810

    返回值:
        data: {submitStatus: true}
        httpstatus: 200
        messages: []
        status: true
        validateMessages: {}
        validateMessagesShowId: "_validatorMessage"
```

