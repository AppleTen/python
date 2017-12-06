def fibs(n):
    a,b = 0,1
    c = 0
    while c < n:
        num = a
        print(num)
        c += 1
        a,b = b,a+b
number = int(input("请输入你要显示的斐波那契数列个数:"))
fibs(number)
