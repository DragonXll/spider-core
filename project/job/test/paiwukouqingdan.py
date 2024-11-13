import requests

cookies = {
    'T-Co': 'uavzfpt',
    'Jk-Token': '0db236047dde4638b185c0ae0cbde2c0',
}

headers = {
    'a-co': 'outlet_huanghe',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'client-type': 'PC',
    'content-type': 'application/json',
    # 'cookie': 'T-Co=uavzfpt; Jk-Token=0db236047dde4638b185c0ae0cbde2c0',
    'jk-token': '0db236047dde4638b185c0ae0cbde2c0',
    'origin': 'https://seemeewes.cn',
    'priority': 'u=1, i',
    'referer': 'https://seemeewes.cn/zhzfpt/uavzfpt/outlet_huanghe/dataManage/pwkDetailedList',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    't-co': 'uavzfpt',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
}

json_data = {
    'current': 1,
    'pageSize': 20,
}

response = requests.post(
    'https://seemeewes.cn/zfpt-api/tenant/pwk/pc/check/searchPcCheckList',
    cookies=cookies,
    headers=headers,
    json=json_data,
)
print(response.text)