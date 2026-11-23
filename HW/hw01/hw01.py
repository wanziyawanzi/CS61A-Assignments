from operator import add, sub

def a_plus_abs_b(a, b):
    """Return a+abs(b), but without calling abs.

    >>> a_plus_abs_b(2, 3)
    5
    >>> a_plus_abs_b(2, -3)
    5
    >>> a_plus_abs_b(-1, 4)
    3
    >>> a_plus_abs_b(-1, -4)
    3
    """
    if b < 0:
        f = sub     #f=sub绑定函数本身,f=sub()绑定了调用结果
    else:
        f = add     #高阶函数的简单应用：让 f 根据条件指向不同函数，最后统一调用 f(a, b)，避免重复代码
    return f(a, b)

def a_plus_abs_b_syntax_check():
    """Check that you didn't change the return statement of a_plus_abs_b.

    >>> # You aren't expected to understand the code of this test.
    >>> import inspect, re
    >>> re.findall(r'^\s*(return .*)', inspect.getsource(a_plus_abs_b), re.M)
    ['return f(a, b)']
    """
    # You don't need to edit this function. It's just here to check your work.


def two_of_three(i, j, k):  #受限表达式、利用内置函数替代控制流
    """Return m*m + n*n, where m and n are the two smallest members of the
    positive numbers i, j, and k.
    
    >>> two_of_three(1, 2, 3)
    5
    >>> two_of_three(5, 3, 1)
    10
    >>> two_of_three(10, 2, 8)
    68
    >>> two_of_three(5, 5, 5)
    50
    """
    return min(i*i+j*j,j*j+k*k,k*k+i*i) #问题可以抽象成对数据的组合、过滤和归约，而不是控制流。

def two_of_three_syntax_check():
    """Check that your two_of_three code consists of nothing but a return statement.

    >>> # You aren't expected to understand the code of this test.
    >>> import inspect, ast
    >>> [type(x).__name__ for x in ast.parse(inspect.getsource(two_of_three)).body[0].body]
    ['Expr', 'Return']
    """
    # You don't need to edit this function. It's just here to check your work.


def largest_factor(n):  # 循环、因数分解、边界处理
    """Return the largest factor of n that is smaller than n.  #返回最大真因子

    >>> largest_factor(15) # factors are 1, 3, 5
    5
    >>> largest_factor(80) # factors are 1, 2, 4, 5, 8, 10, 16, 20, 40
    40
    >>> largest_factor(13) # factor is 1 since 13 is prime
    1
    """
    "*** YOUR CODE HERE ***"
    if n == 1:
        return None
    i=n-1
    for _ in range(0,n-1):
        if n%i == 0 :
            return i
        i=i-1


def hailstone(n):   #while 循环、序列生成、计数
    """Print the hailstone sequence starting at n and return its
    length.

    >>> a = hailstone(10)
    10
    5
    16
    8
    4
    2
    1
    >>> a
    7
    >>> b = hailstone(1)
    1
    >>> b
    1
    """
    "*** YOUR CODE HERE ***"
    i=1 
    print(n)
    while n!=1: #使用 while 循环处理次数未知、由终止条件控制的迭代（与 for 循环的区别）
        if n%2==0:
            n=n//2
        else:
            n=3*n+1
        i+=1
        print(n)
    return i
#从不同角度锻炼了“没有 if 怎么表达逻辑”、“怎么用函数抽象重复”、“循环该选 for 还是 while”等基本功
# 为后面更复杂的递归、数据结构和高阶函数铺路