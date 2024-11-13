import requests

def getTicket() :
    headers = {
        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://103.239.155.212:30038',
        'Referer': 'http://103.239.155.212:30038/shencai-psp-web/web/psp/loginRunner/8fbafc76242d43c38d1d2e01151c0630',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    data = {
        'loginName': '370212',
        'password': '59a5abf530313823c15488ea00ea8385cd37e7351e79c4093cea1e57ce24d3438b85b961e72639b1fc55e8271a3fa7208085dc5e45f31c500687024293b291eebaf0774866d40a34a9926446893883ca0c7a69fd992d97fb4a5025caf2882ede2e7dc42a034b74677f3f743a8c62b07b2ed63ace656036b861a3f05dfce0db38',
    }

    response = requests.post(
        'http://103.239.155.212:30038/shencai-qd-web//service/psp/common/pspProdAuthMainApi/login',
        headers=headers,
        data=data,
        verify=False,
    )
    ticket = response.json()["data"]
    print(ticket)
    return ticket