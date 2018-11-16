

cx.secretStr = cr[0];
cx.buttonTextInfo = cr[1];
cv.train_no = cr[2];
cv.station_train_code = cr[3];
cv.start_station_telecode = cr[4];
cv.end_station_telecode = cr[5];
cv.from_station_telecode = cr[6];
cv.to_station_telecode = cr[7];
cv.start_time = cr[8];
cv.arrive_time = cr[9];
cv.lishi = cr[10];
cv.canWebBuy = cr[11];
cv.yp_info = cr[12];
cv.start_train_date = cr[13];
cv.train_seat_feature = cr[14];
cv.location_code = cr[15];
cv.from_station_no = cr[16];
cv.to_station_no = cr[17];
cv.is_support_card = cr[18];
cv.controlled_train_flag = cr[19];
cv.gg_num = cr[20] ? cr[20] : "--";
cv.gr_num = cr[21] ? cr[21] : "--";    高等软卧
cv.qt_num = cr[22] ? cr[22] : "--";    其他
cv.rw_num = cr[23] ? cr[23] : "--";    软卧
cv.rz_num = cr[24] ? cr[24] : "--";    软座
cv.tz_num = cr[25] ? cr[25] : "--";    特等座
cv.wz_num = cr[26] ? cr[26] : "--";    无座
cv.yb_num = cr[27] ? cr[27] : "--";
cv.yw_num = cr[28] ? cr[28] : "--";    硬卧
cv.yz_num = cr[29] ? cr[29] : "--";    硬座
cv.ze_num = cr[30] ? cr[30] : "--";    二等座
cv.zy_num = cr[31] ? cr[31] : "--";    一等座
cv.swz_num = cr[32] ? cr[32] : "--";   商务座
cv.srrb_num = cr[33] ? cr[33] : "--";  动卧
cv.yp_ex = cr[34];
cv.seat_types = cr[35];
cv.exchange_train_flag = cr[36];
cv.from_station_name = cw[cr[6]];
cv.to_station_name = cw[cr[7]];
cx.queryLeftNewDTO = cv;

1. 火车主要分为两种， 动车/高铁 ，火车
    
    1. 动车类
        - D开头
        - G开头
        
    2. 火车类
        - K开头  快速旅客列车
        - T开头  特快
        - Z开头  直达
        - L开头  临时旅客列车
        - Y开头  旅游列车  

## 座位类型

1. 火车类的座位类型
    - 软卧
    - 硬卧
    - 硬座
    - 无座
        
座位类型|座位编号|座位说明
--|--|--
软卧|4|
硬卧|3|    
硬座|1|
无座|1|无座时，票价与硬座一致，所以为1     
        
    
2. 动车类的座位类型, 支持选座
    
座位类型|座位编号|座位说明|选座编号choose_seatss
--|--|--
一等座|M||1 ABCDF
二等座|O||1 ACDF     
商务座|9|高铁有，动车没有|1 A C F  
高级软卧|A|部分车次有|不可选         
动卧|F|部分车次有|不可选            
    

    