class Account:
    """An account has a balance and a holder.
    一个账户有余额和持有人
    >>> a = Account('John')
    >>> a.deposit(10)
    10
    >>> a.balance
    10
    >>> a.interest
    0.02
    >>> a.time_to_retire(10.25)  # 10 -> 10.2 -> 10.404
    2
    >>> a.balance                # Calling time_to_retire method should not change the balance
    10
    >>> a.time_to_retire(11)     # 10 -> 10.2 -> ... -> 11.040808032
    5
    >>> a.time_to_retire(100)
    117
    """
    max_withdrawal = 10
    interest = 0.02

    def __init__(self, account_holder):
        self.balance = 0
        self.holder = account_holder

    def deposit(self, amount):
        self.balance = self.balance + amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient funds"
        if amount > self.max_withdrawal:
            return "Can't withdraw that amount"
        self.balance = self.balance - amount
        return self.balance

    def time_to_retire(self, amount):
        """Return the number of years until balance would grow to amount.
        接收一个金额，并返回当前余额增长到至少该金额所需的年数.
        假设银行在每年年末将利息（按当前余额乘以利率计算）加到余额中。确保你没有修改账户的余额！"""
        assert self.balance > 0 and amount > 0 and self.interest > 0
        "*** YOUR CODE HERE ***"
        cur_balance = self.balance
        years = 0
        while cur_balance < amount:
            cur_balance *= 1 + Account.interest
            years += 1
        return years


class FreeChecking(Account):
    """A bank account that charges for withdrawals, but the first two are free!
    一个对取款收费的银行账户，但前两次免费！
    >>> ch = FreeChecking('Jack')
    >>> ch.balance = 20
    >>> ch.withdraw(100)  # First one's free. Still counts as a free withdrawal even though it was unsuccessful
    'Insufficient funds'
    >>> ch.withdraw(3)    # Second withdrawal is also free
    17
    >>> ch.balance
    17
    >>> ch.withdraw(3)    # Now there is a fee because free_withdrawals is only 2
    13
    >>> ch.withdraw(3)
    9
    >>> ch2 = FreeChecking('John')
    >>> ch2.balance = 10
    >>> ch2.withdraw(3) # No fee
    7
    >>> ch.withdraw(3)  # ch still charges a fee
    5
    >>> ch.withdraw(5)  # Not enough to cover fee + withdraw
    'Insufficient funds'
    """
    withdraw_fee = 1
    free_withdrawals = 2

    "*** YOUR CODE HERE ***"
    def __init__(self, account_holder):
        super().__init__(account_holder)
        self.with_draw_cnt = 0
    def withdraw(self, amount):
        self.with_draw_cnt += 1
        if self.with_draw_cnt <= FreeChecking.free_withdrawals:           
            return super().withdraw(amount)
        else:
            if amount + FreeChecking.withdraw_fee > self.balance:
                return "Insufficient funds"
            if amount > self.max_withdrawal:
                return "Can't withdraw that amount"
            self.balance = self.balance - amount - FreeChecking.withdraw_fee
            return self.balance


def without(s, i):
    """Return a new linked list like s but without the element at index i.
    "返回一个新的链表，类似于 s，但去掉索引 i 处的元素,原始链表 s 不应被改变
    >>> s = Link(3, Link(5, Link(7, Link(9))))
    >>> without(s, 0)
    Link(5, Link(7, Link(9)))
    >>> without(s, 2)
    Link(3, Link(5, Link(9)))
    >>> without(s, 4)           # There is no index 4, so all of s is retained.
    Link(3, Link(5, Link(7, Link(9))))
    >>> without(s, 4) is not s  # Make sure a copy is created
    True
    """
    "*** YOUR CODE HERE ***"
    def helper(s,i,n):
        if s == Link.empty:
            return s
        if i == n:
            return s.rest
        else:
            return Link(s.first,helper(s.rest,i,n+1))
    return helper(s,i,0)
    '''def without(s, i):   完全可以去掉迭代计数器 n ！
    if s is Link.empty:
        return Link.empty
    if i == 0:
        return s.rest          # 跳过当前节点，共享剩余部分
    return Link(s.first, without(s.rest, i - 1))'''


def duplicate_link(s, val):
    """Mutates s so that each element equal to val is followed by another val.
    接收一个链表 s 和一个值 val。它修改 s，使得每个等于 val 的元素后面都跟着一个额外的 val
    （一份重复副本）。它返回 None。注意不要陷入无限循环，即不断复制新产生的副本！

    注意：为了向链表中插入一个 Link，请重新赋值那些 first 为 val 的 Link 实例的 rest 属性。
    >>> x = Link(5, Link(4, Link(5)))
    >>> duplicate_link(x, 5)
    >>> x
    Link(5, Link(5, Link(4, Link(5, Link(5)))))
    >>> y = Link(2, Link(4, Link(6, Link(8))))
    >>> duplicate_link(y, 10)
    >>> y
    Link(2, Link(4, Link(6, Link(8))))
    >>> z = Link(1, Link(2, (Link(2, Link(3)))))
    >>> duplicate_link(z, 2) # ensures that back to back links with val are both duplicated
    >>> z
    Link(1, Link(2, Link(2, Link(2, Link(2, Link(3))))))
    """
    "*** YOUR CODE HERE ***"
    while s is not Link.empty:
        if s.first == val:
            s.rest = Link(val,s.rest)
            s = s.rest
        s = s.rest
    return None


class Link:
    """A linked list.

    >>> s = Link(1)
    >>> s.first
    1
    >>> s.rest is Link.empty
    True
    >>> s = Link(2, Link(3, Link(4)))
    >>> s.first = 5
    >>> s.rest.first = 6
    >>> s.rest.rest = Link.empty
    >>> s                                    # Displays the contents of repr(s)
    Link(5, Link(6))
    >>> s.rest = Link(7, Link(Link(8, Link(9))))
    >>> s
    Link(5, Link(7, Link(Link(8, Link(9)))))
    >>> print(s)                             # Prints str(s)
    <5 7 <8 9>>
    """
    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest is not Link.empty:
            rest_repr = ', ' + repr(self.rest)
        else:
            rest_repr = ''
        return 'Link(' + repr(self.first) + rest_repr + ')'

    def __str__(self):
        string = '<'
        while self.rest is not Link.empty:
            string += str(self.first) + ' '
            self = self.rest
        return string + str(self.first) + '>'

