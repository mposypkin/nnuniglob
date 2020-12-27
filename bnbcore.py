
def bnb(problem, subs, maxi, f, fi, split):
    eps = problem["eps"]
    fr = None
    xr = None
    i = 0
    sreason = 'solved'
    while len(subs) > 0:
        s = subs.pop()
        c = s.mid()
        fc = f(c)
        # print("fr = ", fr)
        # print(s)
        if xr == None:
            xr = c
            fr = fc
        elif fc < fr:
            xr = c
            fr = fc
        frange = fi(s)
        # print("frange = ", frange)
        if frange[0] < fr - eps:
            subs.extend(split(s))
        i = i + 1
        if i > maxi:
            sreason = "Limit ", maxi, " iteration exceeded\n"
            break
    return {'fr' : fr,  'xr' : xr, 'steps' : i, 'stop' : sreason}
