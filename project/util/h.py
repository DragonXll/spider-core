def _init():
    global _global_dict
    _global_dict = {}


def set_value(key, value):
    # 定义全局变量
    _global_dict[key] = value


def get_value(key):
    # 获取全局变量
    try:
        return _global_dict[key]
    except KeyError:
        return None


def buildHeader():

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': get_value("ASP.NET_SessionId")+'; autoLogin=null; user=null; pwd=null',
        'Origin': 'http://222.135.190.229:8006',
        'Pragma': 'no-cache',
        'Referer': 'http://222.135.190.229:8006/Web6/Report/Statistics/Interflow/EventReport_all.aspx',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    return headers

def buildHeader_zz():
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': 'ASP.NET_SessionId=llon1420qzzt3f3pc3h01dmv; autoLogin=null; user=null; pwd=null',
        'Origin': 'http://60.214.99.139:8006',
        'Referer': 'http://60.214.99.139:8006/WasteGas/RealTime/RealTimeDataQUIDYN/RealTimeData.aspx?type=6',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    return headers

def buildHeader_ls():
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': 'ASP.NET_SessionId=llon1420qzzt3f3pc3h01dmv; autoLogin=null; user=null; pwd=null',
        'Origin': 'http://222.135.190.229:8006',
        'Referer': 'http://222.135.190.229:8006/WasteGas/RealTime/RealTimeDataQUIDYN/RealTimeData.aspx?type=6',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    return headers

def buildCookies():
    cookies = {
        'ASP.NET_SessionId': get_value("ASP.NET_SessionId").replace("ASP.NET_SessionId=",""),
        'autoLogin': 'null',
        'user': 'null',
        'pwd': 'null',
    }
    return cookies

def buildHeader_ls_slagcar_init():
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://ztc-snapshot.qdztc.czczh.cn',
        'Referer': 'https://ztc-snapshot.qdztc.czczh.cn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }
    return headers
def buildHeader_ls_slagcar(accessToken):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Authorization': 'Bearer '+accessToken,
        'Connection': 'keep-alive',
        # 'Cookie': 'cna=d0037901543841f5b549aa6df8c36351',
        'Referer': 'https://ztc-snapshot.qdztc.czczh.cn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }
    return headers

def buildCookies_ls_slagcar():
    cookies = {
        'cna': 'd0037901543841f5b549aa6df8c36351',
    }
    return cookies

def buildCookies_ls_catering():
    cookies = {
        'wanwei_dcloud_AUTH_TOKEN': '{%22access_token%22:%22eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJsc3loIiwiZXhwIjoxNzMxMzk2NDQxLCJqdGkiOiI4OTI0MTk4NDk0IiwiY2xpZW50X2lkIjoiZGNsb3VkLWNsaWVudC1hdXRoIn0.KRHVf9H9jJGT3T2J5kbX_E4Fgi68afZODV9UmXkkHHk%22%2C%22expires_in%22:7199%2C%22scope%22:%22*%22%2C%22timestamp%22:1731389241984%2C%22loginName%22:%22lsyh%22}',
        'wanwei_dcloud_REFRESH_TOKEN': '{%22refresh_token%22:%22eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJsc3loIiwiYXRpIjoiODkyNDE5ODQ5NCIsImV4cCI6MTczMzk4MTI0MSwianRpIjoiODkyNDE5ODQ5NiIsImNsaWVudF9pZCI6ImRjbG91ZC1jbGllbnQtYXV0aCJ9.TBbCEZHPYgg4JzWM6F_vytmZuKy1qL5D34SjC5rD1NI%22%2C%22expires_in%22:7199%2C%22scope%22:%22*%22%2C%22timestamp%22:1731389241984%2C%22loginName%22:%22lsyh%22}',
        'wanwei_dcloud_LOGIN_NAME': 'lsyh',
        'wanwei_dcloud_REGION_CODE': '370212',
    }
    return cookies
def buildHeader_ls_catering():
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJsc3loIiwiZXhwIjoxNzMxMzk2NDQxLCJqdGkiOiI4OTI0MTk4NDk0IiwiY2xpZW50X2lkIjoiZGNsb3VkLWNsaWVudC1hdXRoIn0.KRHVf9H9jJGT3T2J5kbX_E4Fgi68afZODV9UmXkkHHk',
        'Cache-Control': 'no-cache, no-store, max-age=0, must-revalidate',
        'Connection': 'keep-alive',
        # 'Content-Length': '0',
        # 'Cookie': 'wanwei_dcloud_AUTH_TOKEN={%22access_token%22:%22eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJsc3loIiwiZXhwIjoxNzMxMzk2NDQxLCJqdGkiOiI4OTI0MTk4NDk0IiwiY2xpZW50X2lkIjoiZGNsb3VkLWNsaWVudC1hdXRoIn0.KRHVf9H9jJGT3T2J5kbX_E4Fgi68afZODV9UmXkkHHk%22%2C%22expires_in%22:7199%2C%22scope%22:%22*%22%2C%22timestamp%22:1731389241984%2C%22loginName%22:%22lsyh%22}; wanwei_dcloud_REFRESH_TOKEN={%22refresh_token%22:%22eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJsc3loIiwiYXRpIjoiODkyNDE5ODQ5NCIsImV4cCI6MTczMzk4MTI0MSwianRpIjoiODkyNDE5ODQ5NiIsImNsaWVudF9pZCI6ImRjbG91ZC1jbGllbnQtYXV0aCJ9.TBbCEZHPYgg4JzWM6F_vytmZuKy1qL5D34SjC5rD1NI%22%2C%22expires_in%22:7199%2C%22scope%22:%22*%22%2C%22timestamp%22:1731389241984%2C%22loginName%22:%22lsyh%22}; wanwei_dcloud_LOGIN_NAME=lsyh; wanwei_dcloud_REGION_CODE=370212',
        'Expires': '0',
        'Origin': 'http://219.146.67.221:23111',
        'Pragma': 'no-cache',
        'Referer': 'http://219.146.67.221:23111/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }
    return headers