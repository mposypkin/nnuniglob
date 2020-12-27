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
'exsinx' : {'f' : 2 * sin(x) * exp(-x)  , 'ab' : [.2, 7], 'eps' : 1e-3, 'f*' : -0.027864},
'absxsin' : {'f' :  abs(0.25 *(x-1))  + abs(sin(float(pi)*(1 + 0.25 * (x-1)))) + 1, 'ab' : [-10, 10], 'eps' : 1e-3, 'f*' : 1},
'absx110sin' : {'f' :  abs(x-1)  * (1 + 10 * abs(sin(x+1))) + 1, 'ab' : [-10, 10], 'eps' : 1e-3, 'f*' : 1}
}

diff_problems = {
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
'exsinx' : {'f' : 2 * sin(x) * exp(-x)  , 'ab' : [.2, 7], 'eps' : 1e-3, 'f*' : -0.027864}
}


problems_sercas = {
    'exp3xsin3' : {'f' : exp(-3 * x) - sin(x)**3, 'ab' : [0, 20], 'eps' : 1e-3, 'f*' : None},
    '3xsin18x' :{'f' : (3 * x  - 1.4) * sin(18 * x) + 1.7, 'ab' : [0.2, 7], 'eps' : 1e-3, 'f*' : -17.582872},
    '2x2exp200' :{'f' : 2 * x**2 - 0.03 * exp(-(200 * (x - 0.0675))**2), 'ab' : [-10, 10], 'eps' : 1e-3, 'f*' : -0.020903},
    '24x4m142x3' :{'f' : 24 * x**4 - 142 * x**3 + 303 * x**2 - 276 * x + 3, 'ab' : [0, 3], 'eps' : 1e-3, 'f*' : 1}
}

# print(problems['xsin5'])