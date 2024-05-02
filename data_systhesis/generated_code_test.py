def coefficient_of_x3(n, a, b, k):
    from math import factorial
    C = factorial(n) / (factorial(k) * factorial(n - k))
    coefficient = C * a**(n - k) * b**k
    return coefficient

# 参数
n = 6
a = 1
b = 2
k = 3

# 计算系数
coefficient = coefficient_of_x3(n, a, b, k)
print('x^3 项的系数是:', coefficient)