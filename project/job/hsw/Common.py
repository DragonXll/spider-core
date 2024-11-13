import requests
def getCookie(session):
    cookies = {
        'SESSION': session,
        'Hm_lvt_0aabb31005445bec1e2759bd1a8a8485': '1676528819,1676528889,1676534126,1676595887',
        'Hm_lpvt_0aabb31005445bec1e2759bd1a8a8485': '1676595887',
    }
    return cookies


def httpPost(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    }
    return requests.post(url=url, headers=headers)


def httpPostFromData(url, params,session):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': 'Hm_lpvt_0aabb31005445bec1e2759bd1a8a8485=1676595887; SESSION=ab76659a-72d7-432f-a319-7d9d308d66a6; DataCenter_TicketId=sys_ticket_FB15A6C4-C2BF-49B6-96E7-36D30C962398; SECKEY_ABVK=IVOyJPsI7nV5ABhaXwLn8P8YWTXMtbl0+Cm6AJPDCeY%3D; BMAP_SECKEY=X2NdJ1IRuOiJv3qnI6Pw9a7HXRTfHcUM5hc1Mw3OmZpqu0navmrSI8Dc3RUpAlRiYl6qOEeIUvEMP_TW6yNd5Gc6ZW8wsYLCYYCeKkKGQKRNP3F-jVgz4f54njBiTfjnp4405X4WkNHDojeppidHawPfiMs_Ga6S1FsFIJhKql0wJHZLwSsUIxcdDAkxx3LY; Hm_lvt_0aabb31005445bec1e2759bd1a8a8485=1676528889,1676534126,1676595887,1676601781',
        'Origin': 'http://120.221.95.83:6080',
        'Referer': 'http://120.221.95.83:6080/main/view/transfer/wastetransfer/epaSearchList.html?type=WASTE_TRANSFER&ticketId=FB15A6C4-C2BF-49B6-96E7-36D30C962398&orgId=2054298711623680&QUSERXZQ=TXXB6Y3dNakXV5&d=1676601778931&menuCode=EPA_PRO_IN_MANIFEST_LIST1&isShowDeclarationMonth=false',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = params
    response = requests.post(
        url=url,
        data=data,
        cookies=getCookie(session),
        headers=headers,
        verify=False
    )

    print(response.status_code)
    # print(response.json()["data"])
    return response


def httpPostJsonData(url, params,session):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'http://120.221.95.83:6080',
        'Referer': 'http://120.221.95.83:6080/main/view/transfer/wastetransfer/epaSearchList.html?type=WASTE_TRANSFER&ticketId=FB15A6C4-C2BF-49B6-96E7-36D30C962398&orgId=2054298711623680&QUSERXZQ=TXXB6Y3dNakXV5&d=1676601778931&menuCode=EPA_PRO_IN_MANIFEST_LIST1&isShowDeclarationMonth=false',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = params
    response = requests.post(
        url=url,
        json=data,
        cookies=getCookie(session),
        headers=headers,
        verify=False
    )

    print(response.status_code)
    # print(response.json()["data"])
    return response


def httpPostJsonFromData(url, params,session):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://120.221.95.83:6080',
        'Referer': 'http://120.221.95.83:6080/main/view/transfer/wastetransfer/epaSearchList.html?type=WASTE_TRANSFER&ticketId=FB15A6C4-C2BF-49B6-96E7-36D30C962398&orgId=2054298711623680&QUSERXZQ=TXXB6Y3dNakXV5&d=1676601778931&menuCode=EPA_PRO_IN_MANIFEST_LIST1&isShowDeclarationMonth=false',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = params
    response = requests.post(
        url=url,
        cookies=getCookie(session),
        headers=headers,
        data=data,
        verify=False,
    )
    # print(response.json()["data"])
    return response
