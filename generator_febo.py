def febo(n):
    initial = 0
    # 第一个数
    first = 0
    # 第二个数
    second = 1
    # 循环生成斐波那契数列
    while initial < n:
        # 记住first的值
        number = first
        first, second = second, first + second
        initial += 1
        # 使用yield返回迭代器对象，并记录位置
        yield number
#k = febo(5)
for i in febo(5):
    print(i)




