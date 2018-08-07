import os
import sys
import json

from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import AddonFormatError


class FirefoxProfileWithWebExtensionSupport(webdriver.FirefoxProfile):
    def _addon_details(self, addon_path):
        try:
            return super()._addon_details(addon_path)
        except AddonFormatError:
            try:
                with open(os.path.join(addon_path, 'manifest.json'), 'r') as f:
                    manifest = json.load(f)
                    return {
                        'id': manifest['applications']['gecko']['id'],
                        'version': manifest['version'],
                        'name': manifest['name'],
                        'unpack': False,
                    }
            except (IOError, KeyError) as e:
                raise AddonFormatError(str(e), sys.exc_info()[2])


def get_browser_with_proxy():
    proxy_info = {
        "proxy_server": "forward.xdaili.cn:80",
        "proxy_passport": "ZF20185302012bA1trA",
        "proxy_pass": "266ec56b3c304c37b3ce69f4d3357bb7"
    }

    try:

        # profile = webdriver.FirefoxProfile()
        profile = FirefoxProfileWithWebExtensionSupport()

        # add new header
        profile.add_extension("extension")
        webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
            "httpProxy": proxy_info['proxy_server'],
            "sslProxy": proxy_info['proxy_server'],
            "proxyType": "manual",
        }

        profile.update_preferences()

        # 打开 FireFox 浏览器
        firefox_driver_path = r'geckodriver.exe'
        firefox_binary = r'C:\Program Files\Firefox Developer Edition\firefox.exe'
        browser = webdriver.Firefox(profile, executable_path=firefox_driver_path, firefox_binary=firefox_binary)
        return browser
    finally:
        pass


if __name__ == '__main__':
    get_browser_with_proxy()

