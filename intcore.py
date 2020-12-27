# Core interval utils

import math

def neg(x):
    return [-x[1], -x[0]]

def add(x, y):
    y = [x[0] + y[0], x[1] + y[1]]
    return y

def sub(x, y):
    y = [x[0] - y[1], x[1] - y[0]]
    return y

def mul(x, y):
    v = [x[0] * y[0], x[0] * y[1], x[1] * y[0], x[1] * y[1]]
    y = [min(v), max(v)]
    return y

def pow(n, x):
    u = x[0] ** n
    v = x[1] ** n
    y = [min(u, v), max(u, v)]
    if n > 0 and n % 2 == 0 and x[0] <= 0 <= x[1]:
        y[0] = 0
    return y

def sin(x):
    y = [math.sin(x[0]), math.sin(x[1])]
    pi2 = 2 * math.pi
    pi05 = math.pi / 2
    if math.ceil((x[0] - pi05) / pi2) <= math.floor((x[1] - pi05) / pi2):
        ub = 1
    else:
        ub = max(y)
    if math.ceil((x[0] + pi05) / pi2) <= math.floor((x[1] + pi05) / pi2):
        lb = -1
    else:
        lb = min(y)
    return [lb, ub]

def cos(x):
    y = [math.cos(x[0]), math.cos(x[1])]
    pi2 = 2 * math.pi
    if math.ceil(x[0] / pi2) <= math.floor(x[1] / pi2):
        ub = 1
    else:
        ub = max(y)
    if math.ceil((x[0] - math.pi) / pi2) <= math.floor((x[1] - math.pi) / pi2):
        lb = -1
    else:
        lb = min(y)
    return [lb, ub]

def exp(x):
    return [math.exp(x[0]), math.exp(x[1])]

def dpow(n, x, dx):
    y = [0,0]
    if n > 0:
        y = mul([n,n], mul(pow(n-1, x), dx))
    return y

def dmul(x, y, dx, dy):
    return add(mul(x, dy), mul(y, dx))

def dsin(x, dx):
    return mul(cos(x), dx)

def dcos(x, dx):
    return neg(mul(sin(x), dx))

def dexp(x, dx):
    return mul(exp(x), dx)

def ddpow(n, x, dx, ddx):
    y = [0,0]
    if n > 1:
        y = mul([n,n],
                add(
                    mul([n-1, n-1], mul(pow(n-2, x), pow(2,dx))),
                    mul([n,n], mul(pow(n-1, x), ddx))
                )
            )
    return y

def ddmul(x, y, dx, dy, ddx, ddy):
    s1 = mul(ddx, y)
    s2 = mul(ddy, x)
    s3 = mul([2,2], mul(dx, dy))
    return add(s1, add(s2, s3))

def ddsin(x, dx, ddx):
    return sub(mul(cos(x), ddx), mul(sin(x), pow(2, dx)))

def ddcos(x, dx, ddx):
    return neg(add(mul(sin(x), ddx), mul(cos(x), pow(2, dx))))

def ddexp(x, dx, ddx):
    return mul(exp(x), add(pow(2, dx), ddx))

def mid(x):
    return 0.5 * (x[0] + x[1])

def cap(x, y):
    return [max(x[0], y[0]), min(x[1], y[1])]

def first_form(x, dx, c, fc):
    return add(fc, mul(sub(x, c), dx))

