import math
import sys
import intcore as ic
import utils as ut


def not_supported(s):
    sys.exit(s + " is not supported!")

options = {
    'domon' : True,
    'doconv' : True
}

class IntervalDrv:

    def __init__(self, x):
        self.x = x.copy()
        self.dx = [1,1]
        self.ddx = [0,0]
        self.a = x[0]
        self.b = x[1]
        self.fa = x[0]
        self.fb = x[1]
        self.da = 1
        self.db = 1

    def is_mon(self):
        return self.dx[0] >= 0 or self.dx[1] <= 0

    def is_conv(self):
        return self.ddx[0] >= 0

    def is_conc(self):
        return self.ddx[1] <= 0

    def __repr__(self):
        s = "x =[" + str(self.x[0]) + ", " + str(self.x[1]) + "], "
        s += "dx = [" + str(self.dx[0]) + ", " + str(self.dx[1]) + "], "
        s += "ddx = [" + str(self.ddx[0]) + ", " + str(self.ddx[1]) + "], "
        s += "a = " + str(self.a) + ", b = " + str(self.b) + ", "
        s += "fa = " + str(self.fa) + ", fb = " + str(self.fb) + ", "
        s += "da = " + str(self.da) + ", db = " + str(self.db) + ", "
        if self.is_mon():
            s += "monotonic, "
        if self.is_conv():
            s += "convex, "
        if self.is_conc():
            s += "concave, "
        return s

    def mid(self):
        return 0.5 * (self.x[0] + self.x[1])

    def width(self):
        return self.x[1] - self.x[0]

    def scale(self, factor):
        m = 0.5 * (self.x[0] + self.x[1])
        r = 0.5 * (self.x[1] - self.x[0])
        self.x[0] = m - factor * r
        self.x[1] = m + factor * r

    def isIn(self, other):
        return (self.x[0] >= other.x[0]) and (self.x[1] <= other.x[1])

    def isNoIntersec(self, other):
        return (self.x[0] > other.x[1]) or (self.x[1] < other.x[0])

    def intersec(self, other):
        if self.x[0] > self.x[1]:
            raise ValueError(other.x[0], other.x[1], "results in wrong bounds:", self.x[0], self.x[1])
        return IntervalDrv([max(self.x[0], other.x[0]), min(self.x[1], other.x[1])])

    def update_bounds(self, lb, ub, s):
        rv = False
        if lb > self.x[0]:
            # print(s, ": improved lb from ", self.x[0], " to ", lb)
            rv = True
            self.x[0] = lb
        if ub < self.x[1]:
            # print(s, ": improved ub from ", self.x[1], " to ", ub)
            rv = True
            self.x[1] = ub
        # if rv:
        #     print(self)
        return rv

    def monoton_bound(self):
        if options['domon']:
            if self.is_mon():
                lb  = min(self.fa, self.fb)
                ub = max(self.fa, self.fb)
                self.update_bounds(lb, ub, "monoton")

    def conv_bound(self):
        if not options['doconv']:
            return False
        lb = self.x[0]
        ub = self.x[1]
        dlb = self.dx[0]
        dub = self.dx[1]
        s = 'nothing'
        if self.is_conv():
            s = 'convex'
            dlb = self.da
            dub = self.db
            ub = max(self.fa, self.fb)
            if self.da >= 0:
                lb = self.fa
            elif self.db <=0:
                lb = self.fb
            else:
                lb = ut.pijav(self.a, self.b, self.fa, self.fb, self.da, self.db)
        elif self.is_conc() and (self.da > 0) and (self.db < 0):
            s = 'concave'
            dlb = self.db
            dub = self.da
            lb = min(self.fa, self.fb)
            if self.da <= 0:
                ub = self.fa
            elif self.db >= 0:
                ub = self.fb
            else:
                ub = ut.pijav(self.a, self.b, self.fa, self.fb, self.da, self.db)
        xn = ic.cap(self.x, [lb, ub])
        self.x[0] = xn[0]
        self.x[1] = xn[1]
        dn = ic.cap(self.dx, [dlb, dub])
        self.dx[0] = dn[0]
        self.dx[1] = dn[1]


    def improve_bound(self):
        self.monoton_bound()
        self.conv_bound()


    def __getitem__(self, item):
        return self.x[item]

    def __setitem__(self, key, value):
        self.x.__setitem__(key, value)

    def __neg__(self):
        ninterval = IntervalDrv(ic.neg(self.x))
        ninterval.dx = ic.neg(self.dx)
        ninterval.ddx = ic.neg(self.ddx)
        ninterval.a = self.a
        ninterval.b = self.b
        ninterval.fa = - self.fa
        ninterval.fb = - self.fb
        ninterval.da = - self.da
        ninterval.db = - self.db
        ninterval.improve_bound()
        return ninterval

    def __add__(self, other):
        ointerval = valueToInterval(other)
        ninterval = IntervalDrv(ic.add(self.x, ointerval.x))
        ninterval.dx = ic.add(self.dx, ointerval.dx)
        ninterval.ddx = ic.add(self.ddx, ointerval.ddx)
        ninterval.a = self.a
        ninterval.b = self.b
        ninterval.fa = self.fa + ointerval.fa
        ninterval.fb = self.fb + ointerval.fb
        ninterval.da = self.da + ointerval.da
        ninterval.db = self.db + ointerval.db
        ninterval.improve_bound()
        return ninterval

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        ointerval = valueToInterval(other)
        ninterval = IntervalDrv(ic.sub(self.x, ointerval.x))
        ninterval.dx = ic.sub(self.dx, ointerval.dx)
        ninterval.ddx = ic.sub(self.ddx, ointerval.ddx)
        ninterval.a = self.a
        ninterval.b = self.b
        ninterval.fa = self.fa - ointerval.fa
        ninterval.fb = self.fb - ointerval.fb
        ninterval.da = self.da - ointerval.da
        ninterval.db = self.db - ointerval.db
        ninterval.improve_bound()
        return ninterval

    def __rsub__(self, other):
        ointerval = valueToInterval(other)
        return ointerval.__sub__(self)

    def __pow__(self, n):
        y = ic.pow(n, self.x)
        ninterval = IntervalDrv(y)
        ninterval.dx = ic.dpow(n, self.x, self.dx)
        ninterval.ddx = ic.ddpow(n, self.x, self.dx, self.ddx)
        ninterval.a = self.a
        ninterval.b = self.b
        ninterval.fa = self.fa ** n
        ninterval.fb = self.fb ** n
        ninterval.da = n * self.fa ** (n - 1) * self.da
        ninterval.db = n * self.fb ** (n - 1) * self.db
        ninterval.improve_bound()
        return ninterval

    def __mul__(self, other):
        ointerval = valueToInterval(other)
        y = ic.mul(self.x, ointerval.x)
        ninterval = IntervalDrv(y)
        ninterval.dx = ic.dmul(self.x, ointerval.x, self.dx, ointerval.dx)
        ninterval.ddx = ic.ddmul(self.x, ointerval.x, self.dx, ointerval.dx, self.ddx, ointerval.ddx)
        ninterval.a = self.a
        ninterval.b = self.b
        ninterval.fa = self.fa * ointerval.fa
        ninterval.fb = self.fb * ointerval.fb
        ninterval.da = self.fa * ointerval.da + self.da * ointerval.fa
        ninterval.db = self.fb * ointerval.db + self.db * ointerval.fb
        ninterval.improve_bound()
        return ninterval

    def __truediv__(self, other):
        not_supported("division")
        ointerval = valueToInterval(other)
        v = [self.x[0] / ointerval.x[0], self.x[0] / ointerval.x[1], self.x[1] / ointerval.x[0],
             self.x[1] / ointerval.x[1]]
        b = [min(v), max(v)]
        return IntervalDrv(b)

    def __floordiv__(self, other):
        not_supported("floor divsion")
        ointerval = valueToInterval(other)
        if ointerval[0] != 0 and ointerval[1] != 0:
            v = [self.x[0] // ointerval.x[0], self.x[0] // ointerval.x[1], self.x[1] // ointerval.x[0],
                 self.x[1] // ointerval.x[1]]
            print(v)
            b = [min(v), max(v)]
        else:
            ointerval = IntervalDrv([0.001, 0.001])
            v = [self.x[0] // ointerval.x[0], self.x[0] // ointerval.x[1], self.x[1] // ointerval.x[0],
                 self.x[1] // ointerval.x[1]]
            print(v)
            b = [min(v), max(v)]
        return IntervalDrv(b)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __abs__(self):
        not_supported("abs value")
        a = self.x[0]
        b = self.x[1]
        if b <= 0:
            a = -self.x[1]
            b = -self.x[0]
        elif a < 0 < b:
            b = max(-a, b)
            a = 0
        nInt = IntervalDrv([a, b])
        return nInt

#     def __max__(self, other):
#         ointerval = valueToInterval(other)
#         return Interval([max(self.x[0],ointerval.x[0]), max(self.x[1], ointerval.x[1])])

def valueToInterval(expr):
    if isinstance(expr, int) or isinstance(expr, float):
        etmp = IntervalDrv([expr, expr])
        etmp.dx = [0,0]
        etmp.ddx = [0, 0]
        etmp.fa = expr
        etmp.fb = expr
        etmp.da = 0
        etmp.db = 0
    else:
        etmp = expr
    return etmp


def sin(op):
    # not_supported("sin")
    ninterval = IntervalDrv(ic.sin(op.x))
    ninterval.dx = ic.dsin(op.x, op.dx)
    ninterval.ddx = ic.ddsin(op.x, op.dx, op.ddx)
    ninterval.a = op.a
    ninterval.b = op.b
    ninterval.fa = math.sin(op.fa)
    ninterval.fb = math.sin(op.fb)
    ninterval.da = math.cos(op.fa) * op.da
    ninterval.db = math.cos(op.fb) * op.db
    return ninterval


def cos(op):
    ninterval = IntervalDrv(ic.cos(op.x))
    ninterval.dx = ic.dcos(op.x, op.dx)
    ninterval.ddx = ic.ddcos(op.x, op.dx, op.ddx)
    ninterval.a = op.a
    ninterval.b = op.b
    ninterval.fa = math.cos(op.fa)
    ninterval.fb = math.cos(op.fb)
    ninterval.da = - math.sin(op.fa) * op.da
    ninterval.db = - math.sin(op.fb) * op.db
    return ninterval


def exp(op):
    ninterval = IntervalDrv(ic.exp(op.x))
    ninterval.dx = ic.dexp(op.x, op.dx)
    ninterval.ddx = ic.ddexp(op.x, op.dx, op.ddx)
    ninterval.a = op.a
    ninterval.b = op.b
    ninterval.fa = math.exp(op.fa)
    ninterval.fb = math.exp(op.fb)
    ninterval.da = math.exp(op.fa) * op.da
    ninterval.db = math.exp(op.fb) * op.db
    return ninterval




def log(x):
    not_supported("log")
    return IntervalDrv([math.log(x[0]), math.log(x[1])])


# def log(x, base):
#     if base > 1:
#         return Interval([math.log(x[0], base), math.log(x[1], base)])
#     else:
#         return Interval([math.log(x[1], base), math.log(x[0], base)])
#

def i_min(x, y):
    return IntervalDrv([min(x[0], y[0]), min(x[1], y[1])])


def i_max(x, y):
    return IntervalDrv([max(x[0], y[0]), max(x[1], y[1])])