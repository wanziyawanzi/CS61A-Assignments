HW_SOURCE_FILE = __file__


def num_eights(n):
    """Returns the number of times 8 appears as a digit of n.
        返回数字 n 中数字 8 出现的次数。
    >>> num_eights(3)
    0
    >>> num_eights(8)
    1
    >>> num_eights(88888888)
    8
    >>> num_eights(2638)
    1
    >>> num_eights(86380)
    2
    >>> num_eights(12345)
    0
    >>> num_eights(8782089)
    3
    >>> from construct_check import check
    >>> # ban all assignment statements 禁止所有赋值语句
    >>> check(HW_SOURCE_FILE, 'num_eights',
    ...       ['Assign', 'AnnAssign', 'AugAssign', 'NamedExpr', 'For', 'While'])
    True
    """
    "*** YOUR CODE HERE ***"
    if n < 10 :
        if n%10 == 8:
            return 1
        else: 
            return 0
    else:
        return num_eights(n//10)+num_eights(n%10)


def digit_distance(n):
    """Determines the digit distance of n.
        确定相邻数字之间差的绝对值之和
    >>> digit_distance(3)
    0
    >>> digit_distance(777) # 0 + 0
    0
    >>> digit_distance(314) # 2 + 3
    5
    >>> digit_distance(31415926535) # 2 + 3 + 3 + 4 + ... + 2
    32
    >>> digit_distance(3464660003)  # 1 + 2 + 2 + 2 + ... + 3
    16
    >>> from construct_check import check
    >>> # ban all loops 不允许使用 for 循环和 while 循环
    >>> check(HW_SOURCE_FILE, 'digit_distance',
    ...       ['For', 'While'])
    True
    """
    "*** YOUR CODE HERE ***"
    '''if n < 10: return 0  这种切分方式丢失了前导为0的信息
    elif n < 100: return abs(n//10-n%10)
    else: return digit_distance(n//10)+digit_distance(n%100)'''
    #不要把一个数字从中间截断后，再把截出来的部分当作独立的数去处理
    #数字是一串固定位数的数字序列，每次只剥离最后一位，这样相邻差总能在当前层被计算
    if n < 10: 
        return 0
    else: 
        return digit_distance(n//10)+abs(n%100//10-n%10)

def interleaved_sum(n, odd_func, even_func):
    """Compute the sum odd_func(1) + even_func(2) + odd_func(3) + ..., up
    to n. 计算 odd_func(1) + even_func(2) + odd_func(3) + ...的和，直到 n

    >>> identity = lambda x: x
    >>> square = lambda x: x * x
    >>> triple = lambda x: x * 3
    >>> interleaved_sum(5, identity, square) # 1   + 2*2 + 3   + 4*4 + 5
    29
    >>> interleaved_sum(5, square, identity) # 1*1 + 2   + 3*3 + 4   + 5*5
    41
    >>> interleaved_sum(4, triple, square)   # 1*3 + 2*2 + 3*3 + 4*4
    32
    >>> interleaved_sum(4, square, triple)   # 1*1 + 2*3 + 3*3 + 4*3
    28
    >>> from construct_check import check
    >>> check(HW_SOURCE_FILE, 'interleaved_sum', ['While', 'For', 'Mod']) #禁止循环和% ban loops and %
    True
    >>> check(HW_SOURCE_FILE, 'interleaved_sum', ['BitAnd', 'BitOr', 'BitXor']) # ban bitwise operators, don't worry about these if you don't know what they are
    True
    """
    "*** YOUR CODE HERE ***"
    if n == 1:
        return odd_func(1)
    elif n//2*2 == n:
        return even_func(n)+interleaved_sum(n-1,odd_func, even_func)
    else:
        return odd_func(n)+interleaved_sum(n-1,odd_func, even_func)
    


def next_smaller_dollar(bill):
    """Returns the next smaller bill in order.返回按顺序的下一个更小面额的钞票"""
    if bill == 100:
        return 50
    if bill == 50:
        return 20
    if bill == 20:
        return 10
    elif bill == 10:
        return 5
    elif bill == 5:
        return 1

def count_dollars(total):
    """Return the number of ways to make change.
        返回凑出零钱的方法数,从大面额向小面额递归
    >>> count_dollars(15)  # 15 $1 bills, 10 $1 & 1 $5 bills, ... 1 $5 & 1 $10 bills
    6
    >>> count_dollars(10)  # 10 $1 bills, 5 $1 & 1 $5 bills, 2 $5 bills, 10 $1 bills
    4
    >>> count_dollars(20)  # 20 $1 bills, 15 $1 & $5 bills, ... 1 $20 bill
    10
    >>> count_dollars(45)  # How many ways to make change for 45 dollars?
    44
    >>> count_dollars(100) # How many ways to make change for 100 dollars?
    344
    >>> count_dollars(200) # How many ways to make change for 200 dollars?
    3274
    >>> from construct_check import check
    >>> # ban iteration 禁止迭代
    >>> check(HW_SOURCE_FILE, 'count_dollars', ['While', 'For'])
    True
    """
    "*** YOUR CODE HERE ***"
    '''明确函数的定义域和边界。对每个边界值问“答案是什么”。
    确保递归路径最终到达这些边界。必要时用“空选择”或“空操作”来定义基准（如 0 的一种拆分）'''
    def f(n,m):
        if n == 0:
            return 1
        elif n < 0:
            return 0
        elif m == 1:
            return 1
        else:
            return f(n-m,m)+f(n,next_smaller_dollar(m))
    return f(total,100)


def next_larger_dollar(bill):
    """Returns the next larger bill in order.返回按顺序的下一个更大面额的钞票"""
    if bill == 1:
        return 5
    elif bill == 5:
        return 10
    elif bill == 10:
        return 20
    elif bill == 20:
        return 50
    elif bill == 50:
        return 100

def count_dollars_upward(total):
    """Return the number of ways to make change using bills.
        用给定面额的钞票凑出金额,从小面额向大面额递归
    >>> count_dollars_upward(15)  # 15 $1 bills, 10 $1 & 1 $5 bills, ... 1 $5 & 1 $10 bills
    6
    >>> count_dollars_upward(10)  # 10 $1 bills, 5 $1 & 1 $5 bills, 2 $5 bills, 10 $1 bills
    4
    >>> count_dollars_upward(20)  # 20 $1 bills, 15 $1 & $5 bills, ... 1 $20 bill
    10
    >>> count_dollars_upward(45)  # How many ways to make change for 45 dollars?
    44
    >>> count_dollars_upward(100) # How many ways to make change for 100 dollars?
    344
    >>> count_dollars_upward(200) # How many ways to make change for 200 dollars?
    3274
    >>> from construct_check import check
    >>> # ban iteration 禁止迭代
    >>> check(HW_SOURCE_FILE, 'count_dollars_upward', ['While', 'For'])
    True
    """
    "*** YOUR CODE HERE ***"
    def f(n,m):
        if n == 0:
            return 1
        elif m == None:
            return 0    
        elif n < m:
            return 0
        else:
            return f(n-m,m)+f(n,next_larger_dollar(m))
    return f(total,1)


def print_move(origin, destination):
    """Print instructions to move a disk.打印移动一个圆盘的指令"""
    print("Move the top disk from rod", origin, "to rod", destination)

def move_stack(n, start, end):
    """Print the moves required to move n disks on the start pole to the end
    pole without violating the rules of Towers of Hanoi.
    打印将 n 个圆盘从起始柱移动到目标柱所需的步骤，且不违反汉诺塔规则
    n -- number of disks
    start -- a pole position柱子位置, either 1, 2, or 3
    end -- a pole position柱子位置, either 1, 2, or 3

    There are exactly three poles, and start and end must be different. Assume
    that the start pole has at least n disks of increasing size, and the end
    pole is either empty or has a top disk larger than the top n start disks.
    总共恰好有三根柱子，且 start 和 end 必须不同。假设起始柱至少有 n 个尺寸递增的圆盘，
    目标柱要么为空，要么其顶部圆盘比起始柱顶部 n 个圆盘都大
    >>> move_stack(1, 1, 3)
    Move the top disk from rod 1 to rod 3
    >>> move_stack(2, 1, 3)
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 3
    >>> move_stack(3, 1, 3)
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 3 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 1
    Move the top disk from rod 2 to rod 3
    Move the top disk from rod 1 to rod 3
    """
    assert 1 <= start <= 3 and 1 <= end <= 3 and start != end, "Bad start/end"
    "*** YOUR CODE HERE ***"
    if n == 1:
        print_move(start,end)
    else:
        mid = 6-start-end
        move_stack(n-1,start,mid)
        print_move(start,end)
        move_stack(n-1,mid,end)


from operator import sub, mul

def make_anonymous_factorial():
    """Return the value of an expression that computes factorial.
        返回一个计算阶乘的表达式的值。太变态了,完全不会,看AI的
        把函数自己作为参数传进去，让函数“自己调用自己”但通过参数实现
    >>> make_anonymous_factorial()(5)
    120
    >>> from construct_check import check
    >>> # ban any assignments or recursion  禁止任何赋值或递归，不能显示定义函数，换一种方式表达递归
    >>> check(HW_SOURCE_FILE, 'make_anonymous_factorial',
    ...     ['Assign', 'AnnAssign', 'AugAssign', 'NamedExpr', 'FunctionDef', 'Recursion'])
    True
    """
    return (lambda f:lambda n:f(f,n))(lambda self,n: 1 if n==0 else n*self(self,n-1))
    #立即调用的函数表达式,一次性完成“定义、传递、返回”这个过程.(lambda 参数: 函数体)(实际参数)
