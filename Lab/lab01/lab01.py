def digit(n, k):    #纯表达式+整数分解
    """Return the digit that is k from the right of n for positive integers n and k.

    >>> digit(3579, 2)
    5
    >>> digit(3579, 0)
    9
    >>> digit(3579, 10)
    0
    """
    return (n//(10**k))%10  


def middle(a, b, c):     #把选择交给数学性质和内置函数
    """Return the number among a, b, and c that is not the smallest or largest.
    Assume a, b, and c are all different numbers.

    >>> middle(3, 5, 4)
    4
    >>> middle(30, 5, 4)
    5
    >>> middle(3, 5, 40)
    5
    >>> middle(3, 5, 40)
    5
    >>> middle(30, 5, 40)
    30
    """
    return a+b+c-min(a,b,c)-max(a,b,c)


def falling(n, k):  #while 循环 + 累乘 + 边界处理
    """Compute the falling factorial of n to depth k.

    >>> falling(6, 3)  # 6 * 5 * 4
    120
    >>> falling(4, 3)  # 4 * 3 * 2
    24
    >>> falling(4, 1)  # 4
    4
    >>> falling(4, 0)
    1
    """
    "*** YOUR CODE HERE ***"
    i=0;m=1
    while i!=k:
        m=(n-i)*m
        i+=1
    return m

def divisible_by_k(n, k):
    """
    >>> a = divisible_by_k(10, 2)  # 2, 4, 6, 8, and 10 are divisible by 2
    2
    4
    6
    8
    10
    >>> a
    5
    >>> b = divisible_by_k(3, 1)  # 1, 2, and 3 are divisible by 1
    1
    2
    3
    >>> b
    3
    >>> c = divisible_by_k(6, 7)  # There are no integers up to 6 divisible by 7
    >>> c
    0
    """
    "*** YOUR CODE HERE ***"
    i=0;s=0
    if n%k==0:      #生成序列 + 计数
        while s!=n:
            s=s+k
            i+=1
            print(s)
    return i


def sum_digits(y):
    """Sum all the digits of y.

    >>> sum_digits(10) # 1 + 0 = 1
    1
    >>> sum_digits(4224) # 4 + 2 + 2 + 4 = 12
    12
    >>> sum_digits(1234567890)
    45
    >>> a = sum_digits(123) # make sure that you are using return rather than print
    >>> a
    6
    """
    "*** YOUR CODE HERE ***"
    k=1;s=y%10      #从低往高，更加简单。while y > 0: s += y % 10; y //= 10
    while y//(10**k) >0:    #逐位分解 + 累加
        k+=1
    k-=1
    while k!=0:
        s+=y//(10**k)
        y=y-(y//(10**k))*(10**k)
        k-=1        
    return s


def double_eights(n):
    """Return true if n has two eights in a row.
    >>> double_eights(8)
    False
    >>> double_eights(88)
    True
    >>> double_eights(2882)
    True
    >>> double_eights(880088)
    True
    >>> double_eights(12345)
    False
    >>> double_eights(80808080)
    False
    """
    "*** YOUR CODE HERE ***"
    k=1;s=0;x=0
    if n<10:    #逐位扫描 + 相邻判断 + 提前返回
        return False
    else:
        while n//(10**k) >0:
            k+=1
        k-=1
        while k!=0:
            s=n//(10**k)
            n=n-s*(10**k)
            k-=1
            if s==8:
                x=n//(10**k)
                if x==8:
                    return True
        return False

