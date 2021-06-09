x = range(2,201)
for i in x:
    line1 = '   * [nw_%s](https://github.com/nihole/wg_navalny/wiki/nw_%s)' % (str(i), str(i))
    line2 = '   * [pw_%s](https://github.com/nihole/wg_navalny/wiki/pw_%s)' % (str(i), str(i))
    print (line1)
    print (line2)
