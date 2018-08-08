#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by VinChan on 4/12/2018 0012


def quick_sort(array, l, r):
    if l < r:
        q = _partition(array, l, r)
        quick_sort(array, l, q - 1)
        quick_sort(array, q + 1, r)


def partition(array, l, r):
    x = array[r]
    i = l - 1
    for j in range(l, r):
        if array[j] <= x:
            i += 1
            array[i], array[j] = array[j], array[i]
    array[i + 1], array[r] = array[r], array[i + 1]
    return i + 1


def _partition(array, l, r):
    x = array[r]
    i = l
    for j in range(l, r):
        if array[j] <= x:
            array[i], array[j] = array[j], array[i]
            i += 1
    array[i], array[r] = array[r], array[i]
    return i


if __name__ == "__main__":
    ls = [3, 4, 6, 2, 7, 11, 10, 5, 8, 17, 28, 4, 9, 2, 5, 8, 28, 54, 29]
    print(ls, len(ls))
    quick_sort(ls, 0, len(ls) - 1)
    print(ls, len(ls))
