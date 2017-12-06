def feibo(n):
    # 递归斐波那契数列
    if n == 0 or n == 1:
        return 1
    else:
        # 返回的是前两个数的和
        return feibo(n-1) + feibo(n-2)
for i in range(10):
    print(feibo(i))
