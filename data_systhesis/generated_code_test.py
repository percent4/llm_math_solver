import sympy as sp

# 定义变量
x = sp.symbols('x')

# 设置方程
equation = x * (2*x + 3) - 119

# 解方程
sol = sp.solve(equation, x)

# 提取实数根，因为宽度必须为正数
real_solutions = [s.evalf() for s in sol if s.is_real and s > 0]

width = real_solutions[0] if real_solutions else None
length = (2 * width + 3) if width else None

print(width, length)