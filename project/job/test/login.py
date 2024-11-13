import requests

cookies = {
    'T-Co': 'uavzfpt',
}

headers = {
    'a-co': 'login',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'client-type': 'PC',
    'content-type': 'application/json',
    # 'cookie': 'T-Co=uavzfpt',
    'jk-token': '',
    'origin': 'https://seemeewes.cn',
    'priority': 'u=1, i',
    'referer': 'https://seemeewes.cn/zhzfpt/uavzfpt/login',
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
    'captcha': '8dom',
    'checkKey': 'e2274fc50e87304dad09f8d0cc122d34',
    'password': '6fb264a57cc3fd9c61178d0450311c44',
    'username': '18560150520',
}

response = requests.post(
    'https://seemeewes.cn/zfpt-api/tenant/user/login/password',
    cookies=cookies,
    headers=headers,
    json=json_data,
)
print(response.text)