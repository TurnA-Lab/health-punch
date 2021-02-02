# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@file: health_punch.py
@author: Skye Young
@time: 2021/2/2 0002 14:46
"""
from re import search
from time import localtime, strftime

from lxml.html import fromstring
from requests import Session
from requests.adapters import HTTPAdapter

from util import F


class StepErr(Exception):
    """
    添加步骤错误，方便监测状态，以便进行终止等操作
    """

    def __init__(self, *args):
        self.args = args


def inited_session() -> Session:
    """
    初始化 session
    :return: Session
    """
    session = Session()
    # Agent
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'
    })
    # 失败后最多再尝试两次（共三次）
    session.mount('http://', HTTPAdapter(max_retries=2))
    session.mount('https://', HTTPAdapter(max_retries=2))

    return session


def login(session: Session, username: str, password: str) -> Session:
    """
    登录操作，直接使用
    :param session: Session
    :param username: 用户名
    :param password: 密码
    :return: Session
    :raise: StepErr
    """
    # 登录链接
    url = "http://ids2.just.edu.cn/cas/login?service=http://ehall.just.edu.cn/default/work/jkd/jkxxtb/jkxxcj.jsp"
    # 登陆参数
    data = {
        'username': username,
        'password': password,
        # 不知道有什么用的东西,但是不建议删除,猜测大概是用来标记系统运行状态的
        'execution': '0b84a9e5-7bfd-4121-8562-eab0b8461df5_ZXlKaGJHY2lPaUpJVXpVeE1pSjkuTHpCYU9EaDVkek42S3pOMFIxYzNiV05wYWtFeldWbzJVVEo2VmtsaVdsUlpkR05UVlRscGVHNXBUbGRVVXl0TlJEUnhTMXBuVDJSQ2R6a3ZkMEYxU0N0cVlUWm5WR1ZhSzA5RVRETkhjU3M0T1ZsWmExUnBkM1pwWTNWNlNXdzNZVmhyYUZWTGJTdFNObVpWTHpkVmRDdFBUM1pJYms5V2JIWkhlSGQzWWpSSFJrbHRhRU5xV2xOcVRHTnJXa2xQVkU0MVNHZEZXa2hUTUZOc0wyeHpURUoyT1ZOQmNWaGxUVGRCTVVoeWFuaFdORlUzZW5oQkwzUlVaVGRtZHpFdlRHVm9heXN2YnpkUWVGVjVPVGw2V2tKNU15dE9OWFZNVW5seWNGaFNiMFZHV2s5UlEwczVSREJaZVUxcEt6RTVZbFJ3T1haaFIycEZVbUp4ZW1nMWN6ZFJkMWxCTlhWWWNVbDRRbkZOYVN0dmNVYzBkekkyZVRBME0xbElOSE40VDB0UVpsWklORVo2YmpGUldFaHhRM04yYkdnd01rTk1PVTl5TVZkRFRsbDZMMlJvTDNsck9XOTBUbkZJVjFRM05rRnVPSEk1WWtKWVltUjNjRU5IUTJkSWJESTJkRkkyYkVVNGFtOTRWRXBWY0VOSFdqSTNhbHAyVWxkVGJHeHpZalpWU3pCVldYRjBORU5SYTJaUFRGYzFRa000VDBkWk5GRTRXSFJ3SzFwV2QybEVRbFZVWnpaM1dWQkdabXRUU2xneFpWTkZSMVZHYW1SeGNucFRVV3hQWVRWcVMzUnBhMHRJZUV0RE4xQTJaM2xxUjB3eWIwNU9ZV0ZEZURsWVMwWm1iSEZ2UzJsUmFFZGlWRlU1VDJSMGRrSmtkRVJxVFhWMlRrNHZZMmgyT0hCMk55dFBLMmszUVVkaU1VOVNNRXRzTkV4bU9GSk5ha3BZZDFKNlkxVTBSekJtTkhCVVZGUkxWRlJRWldSQmJpczRXamR5U3pCUWFHaFZRa2x5UXpKeE9HdE1XVmRqYWpsRldWTktkRmhTTnpOak5WaDZkR05DUldacE9FbzBPRGhhWlhGWWRtVlpla1F4WWs0cllqZHhSVFFyU0hKcldpOW9lbkpWV21aRlMyeHlNbUZDY0ZVME1sbzRUa3BrYVZWbk5HWTBhalptUkdaYVFsVldRWGsyUTFOSVNVbFdOSFZuWTJRcldrbHFlVUpuVEUxS2QwRXJTaTloUml0Q05XWnZlVFJPYWs5cFUzaHVObXRQYlhJNE5rbFJWMms0T1UxWlIyWkJVM2RhVkVSd1NYbDNRVkZvSzJObmFVbGxXa2RJVUdOcmFUazBlR2xXYzJOdk5qRlBkMHRsZEhKeWFsQjNXV1ZTV2twM1pYbHdOMUZUU1djNVdFVm5ObFJMVkRWWFMwOTBTVkZDTUZwVGJHcElkalpPUjNCdVNqaFFWVlJQUTNGeE5qVktjM05UWlcxVFlWVlFkbVI0YVRadVlVZDBSak55TUZWSU1GcHRVVkZYYld4V1ZTc3dTVGh6VWtGQ1F6UkpjRWRZT1ZwMlVuUTNkRFZKV1VRclYxZHhOeTl1V2s4dlQwdHBOWE5CUzJGUFJrWXhlbGxGYkc5dllYVnZlVTEyYkdaWVQwdGFSalVyVDBzd1F6Tk9VRGRoU21SQ2JGQnlZMmxMZGt3d1RqZDJSaTkyYmtKWWJqWXZlWEZFVVZaMldIQlZWa1pvV2poSU9UUkZRbGRTYlZrek5HWlRURnB6ZWxvclUwNWxja2xIZGpjMU1rVnVXREZVZURZdlF6ZDRSV3BhU0U1blJrVldORXRqSzNSdGJrMHZWaXRGV0d4dWIzWm5ZMEZqY3l0SUswcFpUMWw0V25CSVVteGhOSEJEUmpodWJVOVVjVGM1TUdSSVRXWnhibUZ3T0M5dmJDczJRV3ROVTNoc00xWTVVemxYZWs5UVZWZzRhMmd4YzFsNmRVeGpjbGwwY2paYWIydElVbVpHUkVrd2RFUkhTRmhyZEhwSGRHOVZOblZzVDFJMk0zVTRNWGRMVjFkaFYwaDZhV3huVVc0M01uVnhka0pLVWtObllXTTNkbEJoTlRWNWQyeGxiMWREWms5QlVYaHNkVWh6VmxaVlpVZFFNUzkyYUdSemFXUm9TMU5JUzA4MllUWkVTbkpuU1c1amVYSnRTRTFuYTFWME1ITlJlRVowYkZSM1pURjFPR1JxVlVkaFZHUTNPR293YTNNNU5HdGxabGhSWVdvemQzZHpibmhyWTNWUlRUSjRVbEF3WVRCdlpHNUdWek5vVW1SRlRIa3JPVXRZVGtKaVFsVnpUbWhCTlVwcU9HMUNOVVZsYUZScFYwRmFaalZHVDFwNVFsZE5kRFl3U0c5WVRGRm9iM2MyYzJkTFlWUktORmR3V200MlUyUTVla0p5U1ZGVWFsQkVTV1JEY1ZkeFdVaENTRUZIYkc1VGJrWmpNbnAyVml0TWFteFVjV3g1YlhwMlExcFlUa1pMU1hsc01XaEpla1pXY210WGJYVm5aSFZWVkdweUwwOW1OazF6ZW01MFNWVTNabFo1TUZCeVduQllaM1ZJT0ZwUWNUbFlhSEpvUlhkd2VuWlJRV2xXTldGS0wzaEdSVko1TDJ0NFRWSXdhakZ5ZDBvMWFHWnRkM0J0ZURkelF6UkZkMWMxUXpSR0t6QlJhSEJXU1hCYU9IVTNWRVp1TDNsMGVFUkdhR1ZEYTNwb01FaHdNamxIVkU5eFRFOTRTSEpsUVVSVVVIUjZhRXRuTjA5allrcFlka3B1YURscGEwbENNVkU0VFd4blpHdFpSamRtWTI5SVpFbFZaMVV6V2tWYUszUm9Xbmt3WW5oTVdHSk1PUzhyZW5oeFN5dGtRM0l4ZVdKWVEyaG5UekJWZEdwSlQwcHZVMjFuVWpNMGJ5OXpkMnAwUVZKaGRqbGFNMlpHY0VsRFoyWnJVRkI2ZHk5TmNHWnRReTl5UkRSU2IwOTRNVmszWmpWclFTdGtPV2RPYzNWSVUwbDJVMnhaUWpVck1sWmplREZ0VEV0cWMzZHJXWFZDU0c5WlMxWkpjbmxOZWt4T2NHZEVWaTl3U1hjd05UUmtaVVpGT0haVFdEVmpXalJ0TDJNMGQxUmhZblp3Ykdwb2JrdGhjVmRrTkcxWWNWRnRZbEZTWVZOcldGTmhOSFJhV2pCdFFXaGtkV1o0TkRKVVN6TmhSM0ZRUzA0eFZ6QjVjMVl2VDNWUk5DOWhPRXRqYVV4aWRVcGlNVmdyUm01NE1FSTNhWEl6VTAweFZFVldObTVPVUVWV1dtMUtSM0JrVFdKdlZuWlljVkYxVlVkdGMyODFibEJaVjJ4d2NuZG5jMFpDWTJsT1RVMVdVbUUyYVZac01GbDRkek5XWlU1NWExQTJReXQ1YkZoMFVVaHJkVlp6TTFkM1NVWlpUbVJ1U2tKVGFreG5lRGhCZERVNFVXMVhRa3RvUXpscmMxcDFXRVJ5TW14aVlrNVZhWEp3Y1RKaGVVTjZVVWx3VVdZeWMxa3hXR0p0YkZKeFNXd3ZXREZIYTJRcmVFcG1UMDFWV204cldsSmhhMlp2ZVVRNWNHTTNURXh4VVRSc2RXWkhTbHBZZUhaalUyTjNWREJuZFRKVk1XNXRVa3hpUmpKV1dTOW9RakYzU2l0cE9XSTRTME5LVkdnclVFbzRRazFJWVZKQk1rOXhabkZQYTFoQlZrNU5NVk55YWxsTmRUVTRabGw2WlhnNFpGRk1MMWRZZW10RFUybGpLMUp2VFdKelpVMTZZVVY0U1c1NVlYWnVRblJTT0dGVWFFTllZakkzYlVsVFIxRXdZVEpOUzI1SlNIRk9SVkpSZUZjeWVWWllPVzFaVWtKQ2JsRndWVTVWYzBwTU4zQkdWMUZqVUV4eldVRm9PR3M0ZFVWbFRIWktOSFp6TkVoQ2FFTlVRWFJKWW5nMlFrWkZZMWhtWlVoWGRubzRaVFpxVW05eGJGZG1kVlppWm1OdWNWZzJOMHh2TUdOVGIxTjNjVWhHY2pWcFFrNVFibTV3TDJOb1VXUjJaMnRhYlhwSk0ycEpRa2t6WjJWNE9UTXZjMlJtYjFsamRHMWtTRlZvV0hZd05EVnlXREJNWlcwM05VbFVTbGRHUTJ4dlVFbEhXak5NZFZjMGVFdG5RMjVESzFKT1VHVlNhVlZIVUhSNFQwUXhiRXRXY1c4NGJrMU1aMDkzV21oR2NHeDBabU5uTDNCSlJFMTNPREZoWjNoUVoxY3pSMVI1ZWtOTGVqQmhURms0UjNWRUwyWnhUVmRPTkd4WlozSjFUVnA0T1RCYVNraExNeTlSVDBzeE1rWlRWRGh2YlRONk0wUlVPVWxOVkZONlpGSk9WWFZ6Tm1sbmFuUnVabWhEUm5FMFVUUk9iazFtYW1WUVdrWXdRWGg0WW1WTWNIWjBLMWhIVUZkdE9FUndWakZpU0RsM2VVMUxPWGRSV2toQlFURTJNWGhhTURGQk5uQTFSMUZoUW1KeFZVdHNOVUZIWXpOdE5GSlpORGhoZGtOcVkydzROWGN3UjNkVVpTdG9aVEYxTkZKYVRtRjVlbU50UVhOUFlVWnJaRGR3VVN0RVVFWjJSWGRWUVVkNFkxRjBNek5uZUZKUGJIQmxNMkp5VVdrNU5IUktXbGh2ZEVKR09YVlVSMEZQTlZGdGNYSTRjbW8wVkZWa1prZG5ZeXRHV1hKU05VUTJZVm8xWWpkcE5FcHdiRkkwVnpWU1YzbHBiRTQ0Ymtvdk9WRnBVVVJzYnpONU1WVkthRU5zV2xOQ09XeEVlVzFTYUZsRlYyVkdlREoxUVU5Qk4yRmtlVmRWVTJGdVpGSkxOM1I0YkhOaWJGbFpVSFJYV21WRmIwOTVVVTVGVlRaa1pFaHROa1pCY0UxSVUxSnpkREZQU21ZMFJGRnhVamhsWm5KV1IxQlVSMFE0TDBGSk0xbDRVWHBCUW5Sa01Ya3pXRzFDU2xSUU4zWkhWSEEzUVhKSFFWbG1RekE1VVROQk1rOVZlak5OWVVkQlRIZEZUMW8xVFZOV1dFZDBVWE5MTmpJd2VXaHlOekZVLmNxQzl4di14Y3hRaEN6SVd5bG44MTN6VHZSWEhUSHNObDlhZ2JrVWRsUzZaNEZOd0NBN3dyaFM5NHBkaWM5eFlaSks3c19sbzRvellhbVZBeFJkR0Z3',
        '_eventId': 'submit',
        'loginType': '1',
        'submit': '登 录'
    }

    # 尝试登录
    res = session.post(url, data)
    # 解析 HTML
    tree = fromstring(res.content)
    # 获取用户名，不存在（即失败）则返回空
    username = search('Name = \"(.*)\"', tree.xpath('//script[last()]/text()')[-1]).group(1)

    if username is None:
        raise StepErr("0: 登录失败")
    else:
        return session


def get_time() -> (str, str):
    """
    获取时间
    :return: 填报日期，填报时间
    """
    now = localtime()
    return strftime("%Y-%m-%d", now), strftime("%Y-%m-%d %H:%M", now)


def get_punch_info(session: Session, username: str) -> dict:
    """
    生成填报信息
    :param session: Session
    :param username: 用户名
    :return: 填报信息
    :raise: StepErr
    """
    # 打卡要用的数据，根据原系统中之前的打卡信息更新
    info_data = {'id': 0, "sqrid": "", "sqbmid": "", "rysf": "", "sqrmc": "", "gh": "", "sqbmmc": "", "sfzh": "",
                 "xb": "",
                 "jgshen": "", "jgshi": "", "lxdh": "", "jqdt": "", "czdzshen": "", "czdzshi": "", "czdzqu": "",
                 "czdz": "",
                 "tbrq": "", "jrszd": "", "jrstzk": "", "sfdghtjyq": "", "sfyyqryjc": "", "sfyqgzdyqryjc": "",
                 "sfjcysqzrq": "", "sflz": "", "lzsj": "", "lzjtgj": "", "lzbc": "", "sffz": "", "fhzjsj": "",
                 "fhzjgj": "",
                 "fhzjbc": "", "fztztkdd": "", "glqsrq": '["",""]', "sffr": "", "tw": "", "zwtw": "", "jclx": "",
                 "bz": "", "_ext": "", "tjsj": "", "__type": "sdo:com.sudytech.work.suda.jkxxtb.jkxxtb.TSudaJkxxtb"}

    # 获取今天的时间
    (date, time) = get_time()

    # 查询链接
    url = 'http://ehall.just.edu.cn/default/work/jkd/jkxxtb/com.sudytech.portalone.base.db.queryBySqlWithoutPagecond.biz.ext'
    # 查询参数
    data = {'params': {'empcode': username, 'tbrq': date},
            'querySqlId': 'com.sudytech.work.suda.jkxxtb.jkxxtb.queryNear'}

    # 查询打卡数据
    res = session.post(url, json=data).json()
    # 上次提交的数据
    last_punch = res['list'][0]
    # 先确定今天是否提交过
    # TODO: 在凌晨，lastpunch 似乎并不会更新，可能得做一些额外的处理或提示
    if last_punch['TBRQ'] is date:
        raise StepErr("1: 今日已提交，不再重复提交")
    else:
        # 使用上次的数据填充本次的数据
        for k in info_data.keys():
            if k.upper() in last_punch:
                info_data[k] = last_punch[k.upper()]
        # 更新填报日期和时间
        info_data['tbrq'] = date
        info_data['tbsj'] = time
        # 删除 id
        del info_data['id']

        return info_data


def lets_punch(session: Session, username: str) -> None:
    """
    填报健康信息操作，直接使用
    :param session:
    :param username:
    :return: None
    :raise: StepErr
    """
    # 填报信息链接
    url = "http://ehall.just.edu.cn/default/work/jkd/jkxxtb/com.sudytech.portalone.base.db.saveOrUpdate.biz.ext"
    # 尝试先获取信息
    try:
        data = {'entity': get_punch_info(session, username)}
        res: dict = session.post(url, json=data).json()
        # 需要检查 result 是否存在，因为可能没有
        if 'result' not in res.keys() or res['result'] is not '1':
            raise StepErr('0: 提交失败')
    except StepErr:
        raise


def main():
    username = ''
    password = ''

    try:
        # 这个 assert 啥的有没有都无所谓的啦，只不过看没啥接收数据的难受
        assert inited_session() \
               | F(login, username=username, password=password) \
               | F(lets_punch, username=username) is None
        print(f'{username}健康信息填报成功')
    except StepErr as err:
        print(err)


if __name__ == '__main__':
    main()
