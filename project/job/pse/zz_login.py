import requests
import time
import json
from util import view
from util import h

h._init()


def getSession():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'http://60.214.99.139:8006/indext.aspx?stylecode=',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }
    # 设置sessionId
    response = requests.get('http://60.214.99.139:8006/Login.aspx', headers=headers, verify=False)
    h.set_value("ASP.NET_SessionId", response.headers.get("Set-Cookie").split(";")[0])


def getHuaKuai():

    cookies = {
        'ASP.NET_SessionId': h.get_value("ASP.NET_SessionId").replace("ASP.NET_SessionId=",""),
        'autoLogin': 'null',
        'user': 'null',
        'pwd': 'null',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        # 'Cookie': 'ASP.NET_SessionId=llon1420qzzt3f3pc3h01dmv; autoLogin=null; user=null; pwd=null',
        'Referer': 'http://60.214.99.139:8006/Login.aspx',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    params = {
        'method': 'GetSliderImg',
    }

    response = requests.get(
        'http://60.214.99.139:8006/ajax/SliderValidImg.ashx',
        params=params,
        cookies=cookies,
        headers=headers,
        verify=False,
    )
    data = json.loads(response.text)
    background = data["background"]
    slider = data["slider"]
    h.set_value("code", view.run(background, slider))


def sliderValidImg():

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': h.get_value("ASP.NET_SessionId"),
        'Origin': 'http://60.214.99.139:8006',
        'Pragma': 'no-cache',
        'Referer': 'http://60.214.99.139:8006/Login.aspx',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    params = {
        'method': 'CheckSliderImg',
        'vx': h.get_value("code"),
    }

    response = requests.post(
        'http://60.214.99.139:8006/ajax/SliderValidImg.ashx',
        params=params,
        headers=headers,
        verify=False,
    )
    if str(response.status_code) != '200' and str(json.loads(response.text)['code'] != '0'):
        getSession()
        getHuaKuai()
        sliderValidImg()


def inits():
    getSession()
    getHuaKuai()
    sliderValidImg()
    login()


def login():
    cookies = {
        'ASP.NET_SessionId':  h.get_value("ASP.NET_SessionId").replace("ASP.NET_SessionId=",""),
        'autoLogin': 'null',
        'user': 'null',
        'pwd': 'null',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        # 'Content-Length': '0',
        # 'Cookie': 'ASP.NET_SessionId=llon1420qzzt3f3pc3h01dmv; autoLogin=null; user=null; pwd=null',
        'Origin': 'http://60.214.99.139:8006',
        'Referer': 'http://60.214.99.139:8006/Login.aspx',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    params = {
        'Method': 'CheckLiences',
    }

    response = requests.post('http://60.214.99.139:8006/Ajax/Login.ashx', params=params, cookies=cookies,
                             headers=headers, verify=False)

    cookies = {
        'ASP.NET_SessionId': h.get_value("ASP.NET_SessionId").replace("ASP.NET_SessionId=",""),
        'autoLogin': 'null',
        'user': 'null',
        'pwd': 'null',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': 'ASP.NET_SessionId=llon1420qzzt3f3pc3h01dmv; autoLogin=null; user=null; pwd=null',
        'Origin': 'http://60.214.99.139:8006',
        'Referer': 'http://60.214.99.139:8006/Login.aspx',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    params = {
        'Method': 'CheckLogin',
    }

    data = {
        'p1': '7e689ff357a50844d0a85cf3be3a8455',
        'p2': 'fdfb5dcc8a0bdb9ce831f9fa3caf8ab4',
        'sx': h.get_value("code"),
    }

    response = requests.post(
        'http://60.214.99.139:8006/Ajax/Login.ashx',
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
        verify=False,
    )

    if str(response.text) != 'ok':
        getSession()
        getHuaKuai()
        sliderValidImg()
        login()

