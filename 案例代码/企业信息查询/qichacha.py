import hashlib
import time
import requests

#TODO 该代码收集与网络

def sign_data(data, device_id):
    key = 'fiu92nudv9wqwas0a9pvn0asn093qwtu0gasnfash'
    data['timestamp'] = str(int(time.time()) * 1000)
    data['sign'] = hashlib.md5((device_id + data['timestamp'] + key).encode()).hexdigest()
    return data


def get_access_token(device_id):
    """获取refresh_access_token"""
    data = {
        'appId': 'isoh89bvsoivbiuqw0hcbowipbc9032h',
        'deviceId': device_id,  # 'dcdfeafb9eeb4a9b0e6b2bb36961a98a4e48bf86',
        'deviceType': 'iOS',
        'os': '10.3.3',
        'version': '12.4.2'
    }
    data = sign_data(data, device_id)
    headers = {
        'Host': 'appv3.qichacha.net',
        'User-Agent': 'QiChaCha/12.4.2 (iPhone; iOS 10.3.3; Scale/2.00)',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    url = 'https://appv3.qichacha.net/app/v1/admin/getAccessToken'
    resp = requests.post(url, headers=headers, data=data,verify=False)
    return resp.json()


def get_authorization(refresh_token, device_id):
    """刷新refresh_token，并获取最新authorization"""
    data = {
        'appId': 'isoh89bvsoivbiuqw0hcbowipbc9032h',
        'refreshToken': refresh_token,
    }
    data = sign_data(data, device_id)
    headers = {
        'Host': 'appv3.qichacha.net',
        'User-Agent': 'QiChaCha/12.4.2 (iPhone; iOS 10.3.3; Scale/2.00)',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    url = 'https://appv3.qichacha.net/app/v1/admin/refreshToken'
    resp = requests.post(url, data=data, headers=headers,verify=False)
    return resp.json()


def search(keyword, authorization, device_id):
    """关键词搜素"""
    params = {
        'sortField': '',
        'hasMobilePhone': '',
        'isSortAsc': '',
        'hasSC': '',
        'registCapiBegin': '',
        'pageIndex': '1',
        'hasTM': '',
        'hasShiXin': '',
        'hasIPO': '',
        'isHN': '',
        'pageSize': '20',
        'startDateBegin': '',
        'hasPatent': '',
        'statusCode': '',
        'hasMP': '',
        'hasLQ': '',
        'countyCode': '',
        'hasTE': '',
        'searchKey': keyword,
        'startDateEnd': '',
        'searchIndex': 'default',
        'insuredCntEnd': '',
        'hasFinance': '',
        'hasC': '',
        'currencyCode': '',
        'searchType': '',
        'insuredCntStart': '',
        'hasCI': '',
        'province': '',
        'coyType': '',
        'industryV3': '',
        'hasEmail': '',
        'hasPhone': '',
        'registCapiEnd': '',
        'hasGW': ''
    }
    params = sign_data(params, device_id)
    headers = {
        'Host': 'appv3.qichacha.net',
        'Authorization': 'Bearer ' + authorization,
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'QiChaCha/12.4.2 (iPhone; iOS 10.3.3; Scale/2.00)'
    }
    url = 'https://appv3.qichacha.net/app/v3/base/advancedSearch'
    resp = requests.get(url, params=params, headers=headers,verify=False)
    return resp.json()


def get_detail(key_no, authorization, device_id):
    """获取企业详情"""
    params = {
        'isHotKey': '0',
        'unique': key_no
    }
    params = sign_data(params, device_id)
    headers = {
        'Host': 'appv3.qichacha.net',
        'Authorization': 'Bearer ' + authorization,
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'QiChaCha/12.4.2 (iPhone; iOS 10.3.3; Scale/2.00)'
    }
    url = 'https://appv3.qichacha.net/app/v6/base/getEntDetail'
    resp = requests.get(url, params=params, headers=headers,verify=False)
    return resp.json()


if __name__ == '__main__':
    device_id = 'dcdfeafb9eeb4a9b0e6b2bb36961a98a4e48bf89'
    data = get_access_token(device_id)
    refresh_token = data['result']['refresh_token']
    data = get_authorization(refresh_token, device_id)
    authorization = data['result']['access_token']

    data = search('虎林市振边游船客运服务有限公司', authorization, device_id)

    #data = get_detail('50418a1f8dda71b8911b743c0f3b51f5',authorization, device_id)
    import json
    print(json.loads(json.dumps(data)))

