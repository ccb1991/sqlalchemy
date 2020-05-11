"""
Created by 陈辰柄 
datetime:2020/4/25 22:59
Describe:
"""

a = [1, 2, 3, -4, -1, 31, 23, 123, 1, 23]
b = [12, 31, 23, 123, 1, 23, 123, 132]

z = filter(lambda a: a > 0, a)
print(list(z))
