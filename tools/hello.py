import os
import time

command_lib = {
    "connect_devices": "adb devices",
    "wake_up_wechat": "adb shell am start -n com.tencent.mm/.ui.LauncherUI",
    # 发现只要重新唤起一次小程序的Activity，模拟器就自动将他关闭了。很奇怪，不过正好可以利用。
    "shutdown_mini_app": "adb shell am start -n com.tencent.mm/.plugin.appbrand.ui.AppBrandUI",
    # 模拟点击坐标
    "goto_discover": "adb shell input tap 449 1232",
    "mini_programs": "adb shell input tap 236 830",
    "click_qichacha": "adb shell input tap 280 280",
    "login_qichacha": "adb shell input tap 357 579",
    "send_message": "adb shell input tap 65 216"
}


def command_execute(command, check_word=''):
    result = os.popen(command_lib[command]).read()
    if not check_word or not result:
        print("{0} success！".format(command))
        return True
    if check_word in result:
        print("{0} success！".format(command))
        return True
    else:
        print("{0} failed！".format(command))
        print(result)
        return False


def restart_mini_app():
    # check connection
    ok = command_execute("connect_devices", "emulator-5554	device")
    if not ok:
        return None
    # shutdown mini app
    command_execute("shutdown_mini_app", "Starting: Intent")
    time.sleep(0.5)
    # wake up wechat
    command_execute("wake_up_wechat", "Starting: Intent")
    time.sleep(2)
    # click qichacha
    command_execute("click_qichacha")
    print("waiting for mini app loading...")
    time.sleep(6)
    # login qichacha
    command_execute("login_qichacha")


def resend_message():
    # check connection
    ok = command_execute("connect_devices", "emulator-5554	device")
    if not ok:
        return None
    command_execute("send_message")


def wakeup_wechat_and_show_apps():
    ok = command_execute("connect_devices", "emulator-5554	device")
    if not ok:
        return None
    command_execute("wake_up_wechat", "Starting: Intent")
    time.sleep(1.5)
    # goto discover
    command_execute("goto_discover")
    time.sleep(1)
    # show the mini programs list
    command_execute("mini_programs")


if __name__ == '__main__':
    # restart_mini_app()
    wakeup_wechat_and_show_apps()
