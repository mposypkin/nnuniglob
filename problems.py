from sympy import *

x = symbols('x')
problems = {
'xxsq1' : {'f' : (x - x**2)**2 + (x - 1)**2, 'ab' : [-10, 10], 'eps' : 1e-3, 'f*' : 0},
'x4x3x2x' : {'f' : x**4 - 10 * x**3 + 35 * x**2 - 50 * x + 24, 'ab' : [-10, 20], 'eps' : 1e-3, 'f*' : -1},
'sin103' : {'f' : sin(x) + sin(10/3 * x), 'ab' : [2.7, 7.5], 'eps' : 1e-3, 'f*' : None},
'xsin3x1' : {'f' : sin(3 * x) - x - 1, 'ab' : [0, 6.5], 'eps' : 1e-3, 'f*' : None},
'xsin5x' : {'f' : x + sin(5 * x), 'ab' : [.2, 7], 'eps' : 1e-3, 'f*' : -0.077590},
'expsin2pi' : {'f' : exp(-x) - sin(2 * float(pi) * x), 'ab' : [.2, 7], 'eps' : 1e-3, 'f*' : -0.478362},
'x220cos' : {'f' : x**2 / 20 - sin(x + float(pi)/2) + 2, 'ab' : [-10, 20], 'eps' : 1e-3, 'f*' : 1},
'x2cos18' : {'f' : x**2  - sin(18 * x + float(pi)/2) + 2, 'ab' : [-3, 5], 'eps' : 1e-3, 'f*' : 1},
'cossin5' : {'f' : sin(x + float(pi/2))  - sin(5 * x) + 1, 'ab' : [0.2, 7], 'eps' : 1e-3, 'f*' : -0.952897},
'coscos2' : {'f' : 2 * sin(x + float(pi/2))  + sin(2 * x + float(pi/2)) + 5, 'ab' : [0.2, 7], 'eps' : 1e-3, 'f*' : 3.5},
'absxsin' : {'f' :  abs(0.25 *(x-1))  + abs(sin(float(pi)*(1 + 0.25 * (x-1)))) + 1, 'ab' : [-10, 10], 'eps' : 1e-3, 'f*' : 1},
'absx110sin' : {'f' :  abs(x-1)  * (1 + 10 * abs(sin(x+1))) + 1, 'ab' : [-10, 10], 'eps' : 1e-3, 'f*' : 1},
'exsinx' : {'f' : 2 * sin(x) * exp(-x)  , 'ab' : [.2, 7], 'eps' : 1e-3, 'f*' : -0.027864}
}

# print(problems['xsin5'])