import os

import time
import hmac
import hashlib
import base64
import urllib.parse

def send_message(message,mobile='',isAtAll='false'):
    '''
    示例：由于钉钉限制，每分钟最多发送20条信息，
    #@所有人
    # send_message("send message方法封装,@所有人 ",isAtAll='true')
    #@猴子和洺曦
    send_message("send message方法封装", mobile="猴子,洺曦")
    :param message: 需要发送的消息
    :param mobile: 需要@的人，名称需要在mobiles字典内，才能被@到
    :param isAtAll:  是否@所有人，true 表示@所有人
    :return:
    '''


    mobiles = {
        "猴子": "18600105776",
        "洺曦": "13488792037"
    }##钉钉只能通过手机号@，所有此处做了花名和手机号的对应关系，mobile传的花名，必须在该列表内，后期可以考虑配置化
    mb_num = ""
    if len(mobile)>0:
        mbs = mobile.split(",")

        for i in mbs:
            mb_num = mb_num+mobiles.get(i)+','

    ##### 这一段代码为钉钉提供，用来拼接机器人的安全验证
    timestamp = str(round(time.time() * 1000))
    secret = 'SEC8136dba06eef9d55023da6fa5adb3300d6d8899d2ed6b9648de413f8d06cea14'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    #####

    ### 由于钉钉的SDK只支持python3.7,所以此处使用了curl的请求方式，下面是在拼装curl命令
    temp='''
    curl 'https://oapi.dingtalk.com/robot/send?access_token=2a22aba3a696012d64ba3242614459ec3597b04a58aabecf0d48682411cabe6a&timestamp=%s&sign=%s' \
       -H 'Content-Type: application/json' \
       -d '{"msgtype": "text", 
            "text": {
                 "content": "%s"
            },
            "at": {
                "atMobiles": [
                    %s
                ], 
               "isAtAll": %s 
            }
          }'

    '''%(timestamp,sign,message,mb_num,isAtAll)
    print(temp)

    ####
    os.system(temp)  ##命令执行

if __name__ == '__main__':

    #@所有人
    # send_message("send message方法封装,@所有人 ",isAtAll='true')
    #@猴子和洺曦
    send_message("send message方法封装", mobile="猴子,洺曦")