from sympy import *

x = symbols('x')
problems = {
# problem = {'f' : x**6 - 15 * x**4 + 27 * x**2 + 250, 'a' : -4, 'b' : 4, 'eps' : 1e-3}
# problem = {'f' : log(x) - 0.84 * x + 3, 'ab' : [2.7, 7.5],'eps' : 1e-3}
'xsin5' : {'f' : x + sin(5 * x), 'ab' : [.2, 7], 'eps' : 1e-3}
# problem = {'f' : exp(-x) - sin(2 * float(pi) * x), 'ab' : [.2, 7], 'eps' : 1e-3}
# problem = {'f' : x**2 / 20 - sin(x - float(pi)/2) + 2, 'ab' : [-20, 20], 'eps' : 1e-1}
}
print(problems['xsin5'])