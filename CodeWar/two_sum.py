#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Vin on 2017/10/18


class Solution(object):
    @staticmethod
    def two_sum(nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        对比过的数据保存在字典，之后可以快速查找实现O(n)效率
        """
        if len(nums) < 1:
            return False
        num_dict = {}
        for i in range(len(nums)):
            if nums[i] in num_dict:
                return [num_dict[nums[i]], i]
            else:
                num_dict[target - nums[i]] = i


if __name__ == '__main__':
    print(Solution().two_sum([3, 9, 4, 5, 7, 9, 4, 3, 6], 13))
