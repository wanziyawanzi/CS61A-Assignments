from operator import add, mul

square = lambda x: x * x

identity = lambda x: x

triple = lambda x: 3 * x

increment = lambda x: x + 1


HW_SOURCE_FILE=__file__


def product(n, term):
    """Return the product of the first n terms in a sequence.
        返回序列中前 n 项的乘积。
    n: a positive integer 一个正整数
    term:  a function that takes one argument to produce the term
            一个接受一个参数并产生该项的函数
    >>> product(3, identity)  # 1 * 2 * 3
    6
    >>> product(5, identity)  # 1 * 2 * 3 * 4 * 5
    120
    >>> product(3, square)    # 1^2 * 2^2 * 3^2
    36
    >>> product(5, square)    # 1^2 * 2^2 * 3^2 * 4^2 * 5^2
    14400
    >>> product(3, increment) # (1+1) * (2+1) * (3+1)
    24
    >>> product(3, triple)    # 1*3 * 2*3 * 3*3
    162
    """
    "*** YOUR CODE HERE ***"
    i,total=1,1
    while i <= n:
        total *= term(i)
        i+=1
    return total


def accumulate(fuse, start, n, term):
    """Return the result of fusing together the first n terms in a sequence 
    and start.  The terms to be fused are term(1), term(2), ..., term(n). 
    The function fuse is a two-argument commutative & associative function.
    返回将序列中前 n 项与 start 融合在一起的结果。
    要融合的项是 term(1)、term(2)、……、term(n)。
    函数 fuse 是一个接受两个参数、满足交换律和结合律的函数。
    >>> accumulate(add, 0, 5, identity)  # 0 + 1 + 2 + 3 + 4 + 5
    15
    >>> accumulate(add, 11, 5, identity) # 11 + 1 + 2 + 3 + 4 + 5
    26
    >>> accumulate(add, 11, 0, identity) # 11 (fuse is never used)
    11
    >>> accumulate(add, 11, 3, square)   # 11 + 1^2 + 2^2 + 3^2
    25
    >>> accumulate(mul, 2, 3, square)    # 2 * 1^2 * 2^2 * 3^2
    72
    >>> # 2 + (1^2 + 1) + (2^2 + 1) + (3^2 + 1)
    >>> accumulate(lambda x, y: x + y + 1, 2, 3, square)
    19
    """
    "*** YOUR CODE HERE ***"
    #盲点：把‘累计初始值’默认成具体运算的单元，没把start识别为累加器的起点
    i = 1
    acc = start
    while  i <= n:
        acc = fuse(acc,term(i))
        i += 1
    return acc
     


def summation_using_accumulate(n, term):
    """Returns the sum: term(1) + ... + term(n), using accumulate.
        使用 accumulate返回和: term(1) + ... + term(n)
    >>> summation_using_accumulate(5, square) # square(1) + square(2) + ... + square(4) + square(5)
    55
    >>> summation_using_accumulate(5, triple) # triple(1) + triple(2) + ... + triple(4) + triple(5)
    45
    >>> # This test checks that the body of the function is just a return statement.
    >>> # 这个测试检查函数体是否只是一个 return 语句
    >>> import inspect, ast
    >>> [type(x).__name__ for x in ast.parse(inspect.getsource(summation_using_accumulate)).body[0].body]
    ['Expr', 'Return']
    """
    return accumulate(add,0,n,term)


def product_using_accumulate(n, term):
    """Returns the product: term(1) * ... * term(n), using accumulate.
        使用 accumulate 返回乘积: term(1) * ... * term(n)
    >>> product_using_accumulate(4, square) # square(1) * square(2) * square(3) * square(4)
    576
    >>> product_using_accumulate(6, triple) # triple(1) * triple(2) * ... * triple(5) * triple(6)
    524880
    >>> # This test checks that the body of the function is just a return statement.
    >>> import inspect, ast
    >>> [type(x).__name__ for x in ast.parse(inspect.getsource(product_using_accumulate)).body[0].body]
    ['Expr', 'Return']
    """
    return accumulate(mul,1,n,term)


def make_repeater(f, n):
    """Returns the function that computes the nth application of f.
        返回一个函数，该函数计算 f 应用 n 次的结果
    >>> add_three = make_repeater(increment, 3)
    >>> add_three(5)
    8
    >>> make_repeater(triple, 5)(1) # 3 * (3 * (3 * (3 * (3 * 1))))
    243
    >>> make_repeater(square, 2)(5) # square(square(5))
    625
    >>> make_repeater(square, 3)(5) # square(square(square(5)))
    390625
    """
    "*** YOUR CODE HERE ***"
    #逐步提供参数，从而创建更小、更专注的函数
    def term(x):
        i = 1
        acc=f(x)
        while i < n:
            acc = f(acc)
            i += 1 
        return acc
    return term 

