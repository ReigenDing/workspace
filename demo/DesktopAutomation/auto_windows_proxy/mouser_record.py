#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Vin on 2017/8/8

import os
import time
import json
import pyautogui

pyautogui.PAUSE = 0.1
pyautogui.FAILSAFE = True

pyautogui.size()
# (1366, 768)
width, height = pyautogui.size()


def main():
    for i in range(10):
        pyautogui.moveTo(300, 300, duration=0.01)
        pyautogui.moveTo(400, 300, duration=0.01)
        pyautogui.moveTo(400, 400, duration=0.01)
        pyautogui.moveTo(300, 400, duration=0.01)


def save_as(record=None):
    with open('record.html', 'a') as fp:
        fp.write(record)
        fp.write('\n')


def real_position():
    try:
        while True:
            pos = pyautogui.position()
            save_as(pos)
            time.sleep(0.1)
            print(pos)
    except KeyboardInterrupt:
        print('\nExit.')


def load_record(file_path=None):
    file_path = os.path.join('record.html') if file_path is None else file_path
    with open(file_path, 'r') as fp:
        data = json.loads(fp.read())
    return data


def replay(move_list=None):
    move_list = move_list if move_list else []
    for pos in move_list:
        pyautogui.moveTo(*pos, duration=0.1)


if __name__ == '__main__':
    # main()
    os.system('c:/test/upload.exe')
    # real_position()
    # _moves = load_record()
    # replay(_moves)

