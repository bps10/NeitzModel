from __future__ import division

def normPowerlaw(xlen, exponent=2.0):
    x = range(1,int(xlen)+1)
    pow = []
    for val in x:
        pow.append(1.0 / (val**exponent))
    sumPow = sum(pow)
    for i,val in enumerate(pow):
        pow[i] = val / sumPow
    return pow

