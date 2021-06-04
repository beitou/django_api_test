json11 = {"data": {"num": 1, "numFound": 958,
                   "searchTags": [{"cityCode": "110100", "cond": {"radius": "10"}, "label": "附近手艺人", "type": 1}],
                   "start": 0}, "processTime": 0, "success": "true"}

json22 = {
    "data": {
        "num": 1,
        "num2": 1,
        "numFound": 958,
        "searchTags": [{"cityCode": "110102", "cond": {"radius": "10"}, "label": "附近手艺人", "type": 1}]
    }
}

key_error = []
value_error = []
import json


##验证json的key和value的值，一种是包含验证，一种是完全校验
def check_json_key_value(src_data, dst_data, is_value_verify=False):
    if isinstance(src_data, dict):
        for i in src_data:
            if i not in dst_data:
                key_error.append(i + " : " + "匹配失败")
            else:
                if isinstance(src_data[i], dict) and isinstance(dst_data[i], dict):
                    key_error.append(i + " : " + "匹配成功")
                    check_json_key_value(src_data[i], dst_data[i], is_value_verify)
                elif isinstance(src_data[i], list) and isinstance(dst_data[i], list):
                    key_error.append(i + " : " + "匹配成功")
                    for index in range(0, len(src_data[i])):
                        if isinstance(src_data[i][index], dict) and isinstance(dst_data[i][index], dict):
                            check_json_key_value(src_data[i][index], dst_data[i][index], is_value_verify)
                elif isinstance(src_data[i], (int, str, bool)) and isinstance(dst_data[i], (int, str, bool)):
                    if is_value_verify:
                        if src_data[i] != dst_data[i]:
                            value_error.append(
                                "key:" + i + ",期望结果: " + str(src_data[i]) + ", 实际结果: " + str(dst_data[i]))

                    key_error.append(i + " : " + "匹配成功")
                else:
                    key_error.append(i + " : " + "未匹配到")
        return key_error, value_error
    return


def getJsonValue(josnObject, key):
    if key in josnObject:
        return josnObject[key]
    else:
        for i in josnObject:
            if type(josnObject[i]) == dict or type(josnObject[i]) == list:
                return getJsonValue(josnObject[i], key)


def get_json_value(josnObject, key_dir='', isList=False):
    '''
    根据传入的json路径，获取json串中的值
    :param josnObject:
    :param key_dir:
    :param isList:
    :return:
    '''
    len_key_dir = len(key_dir.split('.'))
    temp = key_dir.split('.')
    if type(josnObject) ==str:
        josnObject = json.loads(josnObject)
    for i in range(0, len_key_dir):
        if i == len_key_dir - 1:
            if isList:
                return josnObject[i]
            else:
                return josnObject.get(temp[i])
        else:
            if isList:
                if type(josnObject[i]) == dict:
                    return get_json_value(josnObject[i], key_dir.replace(temp[i] + '.', ''))
                elif type(josnObject[i]) == list:
                    return get_json_value(josnObject[i], key_dir.replace(temp[i] + '.', ''), True)

            else:
                if type(josnObject[temp[i]]) == dict:
                    return get_json_value(josnObject[temp[i]], key_dir.replace(temp[i] + '.', ''))
                elif type(josnObject[temp[i]]) == list:
                    return get_json_value(josnObject[temp[i]], key_dir.replace(temp[i] + '.', ''), True)


if __name__ == '__main__':
    json22='{"data": {"headerUrl": "/upload/20171218/3f7174ecfcb4486e94bfa1a994e37abf", "mobile": "13000000002", "nick": "\u6d4b\u8bd5132_auto", "pushStatus": 1, "refreshToken": "zz8jHtiIPTLdMumxYA0t", "token": "xgarRfw9qJki8nqMBL5J", "tokenExpiration": 1617528065319, "userId": "5380bc86c45048dfb65533e822da6486"}, "processTime": 0, "requestId": "d7b1d434-fb3c-4579-856f-cafb4b8f5728", "serverTime": 1609752065410, "success": true}'
    temp2 = get_json_value(json22, 'data.token')
    print(temp2)
