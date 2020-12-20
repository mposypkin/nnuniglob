import math


class IntConv:

    def __init__(self, x):
        self.x = x.copy()
        self.a = x[0]
        self.b = x[1]
        self.fa = x[0]
        self.fb = x[1]
        self.da = 1
        self.db = 1
        self.conv = True
        self.conc = True
        self.inc = True
        self.dec = False
        self.lin = True
        self.const = False


    def __repr__(self):
        s = "x = [" + str(self.x[0]) + ", " + str(self.x[1]) + "]"
        s = s + ", a = " + str(self.a) + ", b = " + str(self.b)
        s = s + ", fa = " + str(self.fa) + ", fb = " + str(self.fb)
        s = s + ", da = " + str(self.da) + ", db = " + str(self.db)
        if self.const:
            s = s + ', const'
        if self.lin:
            s = s + ', lin'
        if self.inc:
            s = s + ', inc'
        if self.dec:
            s = s + ', dec'
        if self.conv:
            s = s + ', conv'
        if self.conc:
            s = s + ', conc'
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
        return IntConv([max(self.x[0], other.x[0]), min(self.x[1], other.x[1])])

    def conv_bound(self):
        if self.lin:
            self.x[0] = min(self.fa, self.fb)
            self.x[1] = max(self.fa, self.fb)
        elif self.conv and self.da < 0 and self.db > 0:
            self.x[1] = max(self.fa, self.fb)
            cb = (self.db * self.fa - self.da * self.fb + self.da * self.db * (self.b - self.a))/(self.db - self.da)
            if cb > self.x[0]:
                print("cb = ", cb, " > ", self.x[0])
                self.x[0] = cb
        elif self.conc and (self.da > 0) and (self.db < 0):
            self.x[0] = min(self.fa, self.fb)
            cb = (self.db * self.fa - self.da * self.fb + self.da * self.db * (self.b - self.a))/(self.db - self.da)
            if cb < self.x[1]:
                print("cb = ", cb, " < ", self.x[1])
                self.x[1] = cb

    def __getitem__(self, item):
        return self.x[item]

    def __setitem__(self, key, value):
        self.x.__setitem__(key, value)

    def __neg__(self):
        nIntConv = IntConv(self.x)
        nIntConv.x[0] = - self.x[1]
        nIntConv.x[1] = - self.x[0]
        return nIntConv

    def __add__(self, other):
        oIntConv = valueToIntconv(other)
        nIntConv = IntConv(self.x)
        nIntConv.x[0] = self.x[0] + oIntConv.x[0]
        nIntConv.x[1] = self.x[1] + oIntConv.x[1]
        nIntConv.a = self.a
        nIntConv.b = self.b
        nIntConv.fa = self.fa + oIntConv.fa
        nIntConv.fb = self.fb + oIntConv.fb
        nIntConv.da = self.da + oIntConv.da
        nIntConv.db = self.db + oIntConv.db
        nIntConv.const = oIntConv.const and self.const
        nIntConv.lin = oIntConv.lin and self.lin
        nIntConv.inc = oIntConv.inc and self.inc
        nIntConv.dec = oIntConv.dec and self.dec
        nIntConv.conv = oIntConv.conv and self.conv
        nIntConv.conc = oIntConv.conc and self.conc
        nIntConv.conv_bound()
        return nIntConv

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        oIntConv = valueToIntconv(other)
        nIntConv = IntConv(self.x)
        nIntConv.x[0] = self.x[0] - oIntConv.x[1]
        nIntConv.x[1] = self.x[1] - oIntConv.x[0]
        nIntConv.a = self.a
        nIntConv.b = self.b
        nIntConv.fa = self.fa - oIntConv.fa
        nIntConv.fb = self.fb - oIntConv.fb
        nIntConv.da = self.da - oIntConv.da
        nIntConv.db = self.db - oIntConv.db
        nIntConv.const = oIntConv.const and self.const
        nIntConv.lin = oIntConv.lin and self.lin
        nIntConv.inc = oIntConv.dec and self.inc
        nIntConv.dec = oIntConv.inc and self.dec
        nIntConv.conv = oIntConv.conc and self.conv
        nIntConv.conc = oIntConv.conv and self.conc
        return nIntConv

    def __rsub__(self, other):
        oIntConv = valueToIntconv(other)
        return oIntConv.__sub__(self)

    def __pow__(self, other):
        nIntConv = IntConv(self.x)
        u = self.x[0] ** other
        v = self.x[1] ** other
        nIntConv.a = self.a
        nIntConv.b = self.b
        nIntConv.fa = self.fa ** other
        nIntConv.fb = self.fb ** other
        nIntConv.da = other * self.fa ** (other - 1) * self.da
        nIntConv.db = other * self.fb ** (other - 1) * self.db
        if self.const:
            nIntConv.const = True
            nIntConv.lin = True

        if other % 2 == 0:
            if self.x[0] >= 0:
                nIntConv.inc = self.inc
                nIntConv.dec = self.dec
            elif self.x[0] <= 0:
                nIntConv.inc = self.dec
                nIntConv.dec = self.inc
        else:
            nIntConv.inc = self.inc
            nIntConv.dec = self.dec

        if other % 2 == 0:
            if self.x[0] >= 0 and self.conv:
                nIntConv.conv = True
                nIntConv.conc = False
            elif self.x[1] <= 0 and self.conc:
                nIntConv.conv = True
                nIntConv.conc = False
            elif self.lin:
                nIntConv.conv = True
                nIntConv.conc = False
            else:
                nIntConv.inc = False
                nIntConv.dec = False
        else:
            if self.x[0] >= 0 and self.conv:
                nIntConv.conv = True
                nIntConv.conc = False
            elif self.x[1] <= 0 and self.conc:
                nIntConv.conv = False
                nIntConv.conc = True
            else:
                nIntConv.inc = False
                nIntConv.dec = False

        if other == 0:
            nIntConv.x[0] = 1
            nIntConv.x[1] = 1
        elif other % 2 == 0:
            nIntConv.x[1] = max(u, v)
            if self.x[0] <= 0 and self.x[1] >= 0:
                nIntConv.x[0] = 0
            else:
                nIntConv.x[0] = min(u, v)

        else:
            nIntConv.x[0] = u
            nIntConv.x[1] = v

        nIntConv.lin = False
        nIntConv.conv_bound()
        return nIntConv

    def __mul__(self, other):
        oIntConv = valueToIntconv(other)
        nIntConv = IntConv(self.x)
        nIntConv.const = self.const and oIntConv.const
        nIntConv.lin = (self.lin and oIntConv.const) or (self.const and oIntConv.lin) or (self.const and oIntConv.const)
        nIntConv.inc = False
        nIntConv.dec = False

        noval = 1000
        fs = 0
        if self.x[0] >= 0:
            fs += 1
        if self.x[1] <= 0:
            fs -= 1
        if self.x[0] < 0 < self.x[1]:
            fs = noval
        gs = 0
        if oIntConv.x[0] >= 0:
            gs += 1
        if oIntConv.x[1] <= 0:
            gs -= 1
        if oIntConv.x[0] < 0 < oIntConv.x[1]:
            gs = noval

        dfs = 0
        if self.inc:
            dfs += 1
        if self.dec:
            dfs -= 1
        if not self.inc and not self.dec:
            dfs = noval
        dgs = 0
        if oIntConv.inc:
            dgs += 1
        if oIntConv.dec:
            dgs -= 1
        if not oIntConv.inc and not oIntConv.dec:
            dgs = noval

        ss = fs * dgs + gs * dfs
        if -noval/2 < ss < noval/2:
            if ss > 0:
                nIntConv.inc = True
                nIntConv.dec = False
            elif ss < 0:
                nIntConv.inc = False
                nIntConv.dec = True
            else:
                nIntConv.inc = True
                nIntConv.dec = True
        else:
            nIntConv.inc = False
            nIntConv.dec = False

        cfs = 0
        if self.conv:
            cfs += 1
        if self.conc:
            cfs -= 1
        if not self.conv and not self.conv:
            cfs = noval
        cgs = 0
        if oIntConv.conv:
            cgs += 1
        if oIntConv.conc:
            cgs -= 1
        if not oIntConv.conv and not oIntConv.conv:
            cgs = noval

        print(fs, dfs, cfs, gs, dgs, cgs)
        s1 = cfs * gs
        s2 = dfs * dgs
        s3 = cgs * fs
        mins = min(s1, s2, s3)
        maxs = max(s1, s2, s3)
        print("minmax= ", mins, maxs)
        nIntConv.conv = False
        nIntConv.conc = False
        if -noval/2 < mins and maxs < noval/2:
            if mins >= 0:
                nIntConv.conv = True
            if maxs <= 0:
                nIntConv.conc = True


        nIntConv.a = self.a
        nIntConv.b = self.b
        nIntConv.fa = self.fa * oIntConv.fa
        nIntConv.fb = self.fb * oIntConv.fb
        nIntConv.da = self.fa * oIntConv.da + self.da * oIntConv.fa
        nIntConv.db = self.fb * oIntConv.db + self.db * oIntConv.fb
        v = [self.x[0] * oIntConv.x[0], self.x[0] * oIntConv.x[1], self.x[1] * oIntConv.x[0],
             self.x[1] * oIntConv.x[1]]
        nIntConv.x[0] = min(v)
        nIntConv.x[1] = max(v)
        return nIntConv

    def __truediv__(self, other):
        oIntConv = valueToIntconv(other)
        v = [self.x[0] / oIntConv.x[0], self.x[0] / oIntConv.x[1], self.x[1] / oIntConv.x[0],
             self.x[1] / oIntConv.x[1]]
        b = [min(v), max(v)]
        return IntConv(b)

    def __floordiv__(self, other):
        oIntConv = valueToIntconv(other)
        if oIntConv[0] != 0 and oIntConv[1] != 0:
            v = [self.x[0] // oIntConv.x[0], self.x[0] // oIntConv.x[1], self.x[1] // oIntConv.x[0],
                 self.x[1] // oIntConv.x[1]]
            print(v)
            b = [min(v), max(v)]
        else:
            oIntConv = IntConv([0.001, 0.001])
            v = [self.x[0] // oIntConv.x[0], self.x[0] // oIntConv.x[1], self.x[1] // oIntConv.x[0],
                 self.x[1] // oIntConv.x[1]]
            print(v)
            b = [min(v), max(v)]
        return IntConv(b)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rtruediv__(self, other):
        return self.__truediv__(other)


#     def __max__(self, other):
#         oIntConv = valueToIntConv(other)
#         return IntConv([max(self.x[0],oIntConv.x[0]), max(self.x[1], oIntConv.x[1])])

def valueToIntconv(expr):
    if isinstance(expr, int):
        etmp = IntConv([expr, expr])
        etmp.da = 0
        etmp.db = 0
        etmp.inc = True
        etmp.dec = True
        etmp.lin = True
        etmp.const = True
    elif isinstance(expr, float):
        etmp = IntConv([expr, expr])
        etmp.da = 0
        etmp.db = 0
        etmp.inc = True
        etmp.dec = True
        etmp.lin = True
        etmp.const = True
    else:
        etmp = expr
    return etmp


def sin(x):
    if isinstance(x, int):
        return math.sin(x)
    elif isinstance(x, float):
        return math.sin(x)
    else:
        y = [math.sin(x[0]), math.sin(x[1])]
        pi2 = 2 * math.pi
        pi05 = math.pi / 2
        if math.ceil((x[0] - pi05) / pi2) <= math.floor((x[1] - pi05) / pi2):
            b = 1
        else:
            b = max(y)

        if math.ceil((x[0] + pi05) / pi2) <= math.floor((x[1] + pi05) / pi2):
            a = -1
        else:
            a = min(y)
        return IntConv([a, b])


def cos(x):
    if isinstance(x, int):
        return math.cos(x)
    elif isinstance(x, float):
        return math.cos(x)
    else:
        y = [math.cos(x[0]), math.cos(x[1])]
        pi2 = 2 * math.pi
        if math.ceil(x[0] / pi2) <= math.floor(x[1] / pi2):
            b = 1
        else:
            b = max(y)
        if math.ceil((x[0] - math.pi) / pi2) <= math.floor((x[1] - math.pi) / pi2):
            a = -1
        else:
            a = min(y)
        return IntConv([a, b])


def exp(x):
    return IntConv([math.exp(x[0]), math.exp(x[1])])


def abs(x):
    if x[1] < 0:
        return IntConv([-x[0], -x[1]])
    elif x[0] < 0 and x[1] > 0:
        if -x[0] > x[1]:
            return IntConv([x[1], -x[0]])
        else:
            return IntConv([-x[0], x[1]])
    else:
        return IntConv([x[0], x[1]])


def log(x, base):
    if base > 1:
        return IntConv([math.log(x[0], base), math.log(x[1], base)])
    else:
        return IntConv([math.log(x[1], base), math.log(x[0], base)])


def i_min(x, y):
    return IntConv([min(x[0], y[0]), min(x[1], y[1])])


def i_max(x, y):
    return IntConv([max(x[0], y[0]), max(x[1], y[1])])