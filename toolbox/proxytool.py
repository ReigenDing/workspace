import re
import sys
import time
import hashlib
import random
# third_parts
from requests import Session
# local
from toolbox.config import PROXY_SERVICE


class ProxySession(Session):
    """继承了requests的对象，所以使用方法跟requests一样使用就可以了
    在请求数据前，先调用相应的方法使用设置代理。
    具体使用参看 proxytool.test_proxy()
    """
    def proxy_dynamic_forward(self, proxy_server, proxy_passport, proxy_pass, scheme="http"):
        """设置动态转发代理，可用于 阿布云
        无需编码的简单 HTTP Basic Auth
        :param proxy_server: 转发的 服务器:端口
        :param proxy_passport: 通行证
        :param proxy_pass: 密码
        :param scheme: ["http", "https"]
        """
        proxy_auth = '{scheme}://{proxy_passport}:{password}@{server}'.format(proxy_passport=proxy_passport,
                                                                              password=proxy_pass,
                                                                              server=proxy_server,
                                                                              scheme=scheme)
        proxies = {
            'http': proxy_auth,
            'https': proxy_auth
        }
        self.set_proxies(proxies)
        if scheme == "https":
            self.verify = False

    def proxy_authorization(self, proxy_server, proxy_passport, proxy_pass, scheme="http", auth_string=None):
        """需要签名认证的动态转发代理，可用于迅代理
        :param proxy_server: 转发的 服务器:端口
        :param proxy_passport: 通行证
        :param proxy_pass: 密码
        :param scheme: ["http", "https"]
        :param auth_string: 需要编码的签名字符串
        """
        timestamp = str(int(time.time()))
        sign_text = "orderno={0},secret={1},timestamp={2}".format(proxy_passport,
                                                                  proxy_pass,
                                                                  timestamp)
        is_python3 = (sys.version_info[0] == 3)
        if is_python3:
            sign_text = sign_text.encode()
        sign_md5 = hashlib.md5(sign_text).hexdigest().upper()
        auth = auth_string or "sign={0}&orderno={1}&timestamp={2}".format(sign_md5,
                                                                          proxy_passport,
                                                                          timestamp)
        auth_server = "{scheme}://{server}".format(scheme=scheme, server=proxy_server)
        proxies = {
            'http': auth_server,
            'https': auth_server
        }
        self.headers.update({'Proxy-Authorization': auth})
        self.set_proxies(proxies)
        if scheme == "https":
            self.verify = False

    def proxy_common(self, proxy_server=None, scheme="http", proxy_fetch_api=None):
        """使用普通代理（无需认证）
        允许手动传入proxy_server设置代理，也可以自动从指定api获取代理ip。可以通过设置
        proxy_fetch_api指定获取代理ip的api
        :param proxy_server: 代理服务器地址
        :param proxy_fetch_api: 获取代理服务器ip的web接口
        :param scheme: ["http", "https"]
        """
        if not proxy_server:
            proxy_list = self.get_proxy(proxy_fetch_api)
            if proxy_list:
                proxy_server = random.choice(proxy_list)
            else:
                return
        proxy = proxy_server if 'http' in proxy_server else "{0}://{1}".format(scheme, proxy_server)
        proxies = {
            'http': proxy,
            'https': proxy
        }
        if "https" in proxy_server or scheme == "https":
            self.verify = False
        self.set_proxies(proxies)

    def get_proxy(self, proxy_fetch_api=None):
        """返回代理IP接口, 默认再用无忧代理
        """
        url = proxy_fetch_api or "http://api.ip.data5u.com/dynamic/get.html?order=1d2e99c6aede6f64a211a2d8b77931c8"
        res = self.get(url)
        proxy_pattern = re.compile("(?:https?://)?[\d\.]+:\d+")
        proxy_list = proxy_pattern.findall(res.text)
        # print(proxy_list)
        return proxy_list

    def set_proxies(self, proxies=None):
        self.proxies = proxies


def test_proxy():
    # 搜狐ip地址测试接口
    souhu_proxy_test = 'http://pv.sohu.com/cityjson?ie=utf-8'
    sess = ProxySession()
    abuyun = PROXY_SERVICE['abuyun'][0]
    xdaili = PROXY_SERVICE['xdaili'][0]
    data5u = PROXY_SERVICE['data5u'][0]
    # sess.proxy_dynamic_forward(**abuyun)
    # res = sess.get(souhu_proxy_test)
    # print("阿布云:{0}".format(res.text))
    sess.proxy_authorization(**xdaili)
    res = sess.get(souhu_proxy_test)
    print("迅代理:{0}".format(res.text))
    # sess.proxy_common(proxy_fetch_api=data5u)
    # res = sess.get(souhu_proxy_test)
    # print("无忧代理:{0}".format(res.text))
    # sess.proxy_common(proxy_fetch_api='http://proxy.elecfans.net/proxys.php?key=AXw1KwWIsK&num=10')
    # res = sess.get(souhu_proxy_test, timeout=10)
    # print("其它代理:{0}".format(res.text))


if __name__ == '__main__':
    test_proxy()
