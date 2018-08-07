#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by VinChan on 4/14/2018 0014


def conflict(state, next_x):
    next_y = len(state)
    for i in range(next_y):
        if abs(state[i] - next_x) in (0, next_y - i):
            return True
    return False


def queens(num=8, state=()):
    """八皇后问题（回溯算法的典型案例）
    在8×8格的国际象棋上摆放八个皇后，使其不能互相攻击，
    即任意两个皇后都不能处于同一行、同一列或同一斜线上，问有多少种摆法。
    """
    for pos in range(num):
        if not conflict(state, pos):
            if len(state) == num - 1:
                yield (pos,)
            else:
                for result in queens(num, state + (pos,)):
                    yield (pos,) + result


if __name__ == "__main__":
    for q in queens(8):
        print(q)
