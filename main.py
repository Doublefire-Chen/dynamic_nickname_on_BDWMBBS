import datetime
import requests
from bs4 import BeautifulSoup
import re
import hashlib
import time

##########################配置区############################
username = ""  #用户名
password = ""  #密码
graduate_time = datetime.datetime(2024, 6, 30, 0, 0, 0)  #毕业时间，依次为年，月，日，小时，分钟，秒
###########################################################


def calculate_time():
    # calculate how much time remain when I graduate
    #graduate_time = datetime.datetime(2024, 6, 30, 0, 0, 0)
    nowtime = datetime.datetime.now()
    remain_time = graduate_time - nowtime
    print(remain_time)
    days = remain_time.days
    hours = remain_time.seconds // 3600
    minutes = remain_time.seconds // 60 - hours * 60
    seconds = remain_time.seconds - minutes * 60 - hours * 3600
    remain_time = '🔞🧜‍♀️|\x1b[1;36m%d天%d时%d分%d秒后毕业\x1b[m' % (days, hours,
                                                             minutes, seconds)
    return remain_time


class BBS(object):
    """docstring for BBS"""

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()
        self.replyed_url = []

    def refresh_cookie(self):
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://bbs.pku.edu.cn',
            'Referer': 'https://bbs.pku.edu.cn/v2/mobile/login.php',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua':
            '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }
        import time
        timestamp = int(time.time())
        needhash = self.password + self.username + str(
            timestamp) + self.password
        hl = hashlib.md5()
        hl.update(needhash.encode(encoding='utf8'))
        md5 = hl.hexdigest(
        )  # MD5 hash加密处理 参考：https://blog.csdn.net/m0_49589385/article/details/118400697
        data = {
            'username': self.username,
            'password': self.password,
            'keepalive': '0',
            'time': timestamp,
            't': md5
        }  # 登陆时发送请求包的data初始赋值
        global header  # 申明全局变量
        login = self.session.post('https://bbs.pku.edu.cn/v2/ajax/login.php',
                                  data=data,
                                  headers=headers)  # 发送登陆请求
        if str(login) == '<Response [200]>':  # 判断是否成功发送登录请求
            self.session.cookies.update(
                login.cookies
            )  # 更新cookie 参考：https://www.cnblogs.com/zhongyehai/p/9159641.html
            print("cookie更新成功")

    def check_cookie(self):
        r = self.session.get(
            'https://bbs.pku.edu.cn/v2/mobile/home.php')  # 登录后回到主页
        self.session.cookies.update(r.cookies)
        homepage = BeautifulSoup(r.text, "html.parser")  # 解析
        BBS_id = re.search(r'window.username = ".+"',
                           str(homepage)).group(0).replace('"', '').replace(
                               'window.username = ',
                               '')  # 正则表达式匹配得到id并删去匹配用的多余字符串
        if BBS_id == self.username:
            print("cookie有效，登录用户：" + self.username)  # 提示性输出
        else:
            print("cookie失效，正在尝试重新获取cookie")
            self.refresh_cookie()
            self.check_cookie()

    def update_nickname(self, nickname):
        self.check_cookie()
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://bbs.pku.edu.cn',
            'Referer': 'https://bbs.pku.edu.cn/v2/modify-profile.php',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua':
            '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }
        data = {
            'nickname':
            nickname,
            'birthyear':
            '2002',
            'birthmonth':
            '1',
            'birthday':
            '1',
            'gender':
            'M',
            'ranksys':
            '6',
            'desc':
            '[{"type":"ansi","bold":true,"underline":false,"fore_color":9,"back_color":9,"content":"免责声明：\n"}',
        }
        response = self.session.post(
            'https://bbs.pku.edu.cn/v2/ajax/set_profile.php',
            headers=headers,
            data=data)
        if str(response) == '<Response [200]>':
            print("昵称更新成功")
        else:
            print("昵称更新失败")


MyBBS = BBS(username, password)

while True:
    today_now = datetime.datetime.now()
    today_at_0000 = today_now.replace(hour=0, minute=0, second=0)
    today_at_0130 = today_now.replace(hour=1, minute=30, second=0)
    today_at_0659 = today_now.replace(hour=6, minute=59, second=0)
    today_at_0700 = today_now.replace(hour=7, minute=00, second=0)
    today_at_2359 = today_now.replace(hour=23, minute=59, second=0)
    if (today_at_0000 <= today_now <=
            today_at_0130) or (today_at_0700 <= today_now <= today_at_2359):
        try:
            MyBBS.update_nickname(calculate_time())
        except Exception as e:
            print(f"Error: {e}")
        print("time.sleep(6)")
        time.sleep(6)
    if (today_at_0130 <= today_now <= today_at_0659):
        try:
            MyBBS.update_nickname(calculate_time())
        except Exception as e:
            print(f"Error: {e}")
        print("time.sleep(2.4)")
        time.sleep(2.4)
