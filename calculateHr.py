def clHr(year, rhr):
    e = 0.3
    h = (220 - year - rhr) * e + rhr
    print(h)

print('year:')
year = int(input())
print('rhr:')
rhr = int(input())
print('hr:')
clHr(year, rhr)