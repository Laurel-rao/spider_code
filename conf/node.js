const fs = require('fs');
const path = require('path')

const station_names = require('../../../../Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/e07ca67dc509375375b29956ffec47ce/Message/MessageTemp/b6d29d2258d593002f2358f61ef437a9/File/归档/city');
const pas = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9074';

let a = station_names.split('|');
let name_list = [];
let code_list = [];
let city_list = [];
for (let i=1 ; i<a.length;i+=5){
  name_list.push(a[i]);
  code_list.push(a[i+1])
}
name_list.forEach((item,index)=>{
  city_list[index] = {};
  city_list[index].name = item;
  city_list[index].code = code_list[index]
});

fs.writeFile(path.join(__dirname, './index.json'),JSON.stringify(city_list) , (err) => {
  if (err) {
    console.log(err);
  } else {
    console.log('success');
  }
});
