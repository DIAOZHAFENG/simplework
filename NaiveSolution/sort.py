import math
import time


def insertion_sort(l):
    for i in range(len(l)):
        for j in range(i):
            if l[j] > l[i]:
                num = l[i]
                for k in range(i, j, -1):
                    l[k] = l[k - 1]
                l[j] = num
                break
    return l


def quick_sort(l, s=0, e=None):
    # do sort
    if e is None:
        e = len(l) - 1
    if (not l) or s >= e:
        return
    start = s
    end = e
    while start < end:
        if l[end] > l[s]:
            end -= 1
        elif l[start] <= l[s]:
            start += 1
        else:
            l[start], l[end] = l[end], l[start]
    l[s], l[end] = l[end], l[s]
    quick_sort(l, s, end - 1)
    quick_sort(l, end + 1, e)


def reverse_number(num):
    r = 0
    neg = 1
    if num < 0:
        neg = -1
    while num != 0:
        r *= 10
        r += neg * num % 10
        num = neg * (neg * num // 10)
    return neg * r


def longestPalindrome(s):
    """
    :type s: str
    :rtype: str
    """
    if not s: return ''
    l = s[0]
    dp = [[i == j for i in range(len(s))] for j in range(len(s))]
    for t in range(0, len(s)):
        for h in range(0, t):
            if s[t] == s[h] and (t - h < 3 or dp[h + 1][t - 1]):
                dp[h][t] = True
                if t - h + 1 > len(l):
                    l = s[h: t + 1]
    return l


def zigzag_str(s, n):
    if n < 2: return s
    step = 1
    slot = 0
    ss = ['' for i in range(n)]
    for c in s:
        if slot == n - 1:
            step = -1
        elif slot == 0:
            step = 1
        ss[slot] += c
        slot += step
    from functools import reduce
    return reduce(lambda x, y: x + y, ss, '')


def firstMissingPositive(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    n = len(nums)
    i = 0
    while i < n:
        if nums[i] != i + 1 and 0 < nums[i] <= n:
            idx = nums[i]
            nums[i] = nums[idx - 1]
            nums[idx - 1] = idx
        else:
            i += 1

    for j in range(n):
        if nums[j] != j + 1:
            return j + 1

    return n + 1


class Solution(object):
    def __init__(self):
        self.primes = {2: True}

    def isPrime(self, n):
        if n < 3: return True
        for i in self.primes:
            if n % i == 0:
                return False
            if i > math.sqrt(n):
                break
        self.primes[n] = True
        return True

    def countPrimes(self, n):
        """
        :type n: int
        :rtype: int
        """
        count = 0
        for i in range(2, n):
            if self.isPrime(i):
                count += 1
        return count


def find_duplicates(nums):
    dn = []
    for i in range(len(nums), 0, -1):
        while i != nums[i-1]:
            if nums[i-1] == nums[nums[i-1]-1]:
                dn.append(nums[i-1])
                break
                # return nums[i-1]
            temp = nums[i-1]
            nums[i-1] = nums[temp-1]
            nums[temp-1] = temp
    return dn


def find_duplicate(nums):
    for i in range(len(nums)):
        while i != nums[i]:
            if nums[i] == nums[nums[i]]:
                return nums[i]
            temp = nums[i]
            nums[i] = nums[temp]
            nums[temp] = temp


def fib(n):
    a = 1
    b = 1
    for i in range(n):
        temp = a + b
        a = b
        b = temp
    return b


def mapDecoding(message):
    solutions = [0 for i in range(len(message)+1)]
    if not message: return 1
    if message[0] == '0': return 0
    solutions[0] = 1
    solutions[1] = 1
    for i in range(1, len(message)):
        if message[i] == '0':
            if i - 1 < 0 or int(message[i-1]) > 2 or message[i-1] == '0': return 0
            solutions[i+1] = solutions[i-1]
        elif message[i-1] != '0' and 0 < int(message[i-1:i+1]) < 27:
            solutions[i+1] = solutions[i] + solutions[i-1]
        else:
            solutions[i+1] = solutions[i]
    return solutions[len(message)] % 1000000007


def nx4(n):
    solutions = [[1, 1, 1, 1, 0] for i in range(n)]
    if n < 2: return 1
    solutions[0] = [1, 0, 0, 0, 0]
    for i in range(2, n):
        solutions[i] = [sum(solutions[i-1][:-1]) + solutions[i-2][0],
                        solutions[i-1][0] + solutions[i-1][4],
                        solutions[i-1][0] + solutions[i-1][3],
                        solutions[i-1][0] + solutions[i-1][2],
                        solutions[i-1][1]]
    return sum(solutions[-1][:-1]) + solutions[-2][0]


def n_queen(solution, n=0):
    if n == len(solution):
        print(solution)

    valid_pos = set(range(len(solution)))
    for y in range(n):
        valid_pos -= {solution[y]-n+y, solution[y], solution[y]+n-y}
    for xn in valid_pos:
        solution[n] = xn
        n_queen(solution, n+1)

name = 'a'


def f1():
    print(name)


def f2():
    global name
    name = 'b'
    f1()

f2()
