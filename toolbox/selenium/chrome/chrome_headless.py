from selenium import webdriver


def browser_driver(proxy=None):
    # 设置浏览器参数
    options = webdriver.ChromeOptions()
    options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    # 或者加入环境变量
    chrome_driver_path = 'chromedriver.exe'
    # headless
    # options.add_argument('headless')
    # proxy
    if proxy is not None:
        options.add_argument('--proxy-server={proxy}'.format(proxy=proxy))
    options.add_argument(r'--load-extension=D:\Documents\Git\workspace\tools\chrome\extension')
    # window size
    # options.add_argument('window-size=1200x600')
    driver = webdriver.Chrome(chrome_options=options, executable_path=chrome_driver_path)
    return driver


if __name__ == '__main__':
    chrome = browser_driver()
    chrome.get('https://www.baidu.com')

