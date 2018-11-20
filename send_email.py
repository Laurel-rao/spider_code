# _*_ coding:utf-8 _*_
'''
Author: Laurel-rao
create time:2018/11/16 下午2:47
Remark: 
'''

import smtplib
from email.mime.text import MIMEText

'''
     email 库制作邮件, 制作MIME 对象
     smtplib 发送邮件, 需要eamil制作的对象
'''

location = '13694846652@163.com'
purpose = '1562766937@qq.com'
user = ''
password = ''
subject = "python邮件测试"
content = "你好, 购票已经成功，请在 30 分钟之内付款！！！"
msg = MIMEText(content)
msg['Subject'] = subject
msg['From'] = location
msg["To"] = purpose


smtp = smtplib.SMTP()
smtp.connect('smtp.163.com', 25)
smtp.login(user, password)
smtp.sendmail(location, purpose, msg.as_string())
smtp.quit()