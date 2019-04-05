from collections import deque, defaultdict, Counter, ChainMap
import heapq
from operator import itemgetter
from itertools import groupby


class Solution:

    def question_1(self):
        """
        问题1：将序列分解为单独变量
        问题2：考虑序列长度任意的情况
        解答：任何可迭代对象 (即对象有魔法方法 __iter__())，包括字符串、文件、生成器等，都可以使用赋值操作来分解为单独变量
             唯一要求是个数要吻合
             序列长度任意的情况下，可以使用*表达式，接收的对象也是一个可迭代对象
        """
        sequence = [i for i in range(10)]
        print(sequence.__iter__())
        x, *y = sequence
        print("x: {}, y: {}".format(x, y))

    def question_3(self):
        """
        问题3：保存最后N个元素
        解答：使用数据结构deque双端队列，可以选择指定或不指定大小，只能在两端进行插入弹出操作，时间复杂度仅为O(1)
        补充：list类似于数组，其插入和删除操作复杂度较高
        """
        q = deque(maxlen=3)
        for i in range(10):
            q.appendleft(i)
        print(q)

    def question_4(self):
        """
        问题4：找到最大和最小的N个元素
        解答：模块heapq (堆队列算法模块)，堆在底层是一个列表，特殊之处在于堆顶heap[0]总是最小的那个元素
        """
        nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
        # print(heapq.nlargest(3, nums))
        # print(heapq.nsmallest(3, nums))
        # 更复杂的数据结构
        portfolio = [
            {'name': 'IBM', 'shares': 100, 'price': 91.1},
            {'name': 'AAPL', 'shares': 50, 'price': 543.22},
            {'name': 'FB', 'shares': 200, 'price': 21.09},
            {'name': 'HPQ', 'shares': 35, 'price': 31.75},
            {'name': 'YHOO', 'shares': 45, 'price': 16.35},
            {'name': 'ACME', 'shares': 75, 'price': 115.65}
        ]
        # 取price最小和最大的前3个
        cheap = heapq.nsmallest(3, portfolio, key=lambda x: x['price'])
        expensive = heapq.nlargest(3, portfolio, key=lambda x: x['price'])
        print(cheap)
        print(expensive)

        # 堆 (实现细节来自于heapq文档)
        heap = list(nums)
        # 将heap从list转化为堆
        heapq.heapify(heap)
        while heap:
            print(heapq.heappop(heap))

    def question_5(self):
        """
        问题5：实现优先级队列
        使用堆来实现
        """

        class PriorityQueue:

            def __init__(self):
                self.__queue = []
                self.__index = 0

            def push(self, item, priority):
                heapq.heappush(self.__queue, (-priority, self.__index, item))
                self.__index += 1

            def pop(self):
                return heapq.heappop(self.__queue)[-1]

        class Item:
            def __init__(self, name):
                self.name = name

            def __repr__(self):
                return "Item({!r})".format(self.name)

        q = PriorityQueue()
        q.push(Item('foo'), 1)
        q.push(Item('bar'), 5)
        q.push(Item('spam'), 4)
        q.push(Item('grok'), 1)
        print(q.pop())
        print(q.pop())
        print(q.pop())
        print(q.pop())

    def question_6(self):
        """
        问题6：字典中将键映射到多个值
        defaultdict使用
        ordereddict：底层是一个双向链表，以此来实现有序，但内存开销大
        """
        d = defaultdict(list)
        d['a'].append(1)
        print(d)

    def question_7(self):
        """
        问题7：与字典有关的计算问题
        """
        prices = {'ACME': 45.23,
                  'AAPL': 612.78,
                  'IBM': 205.55,
                  'HPQ': 37.20,
                  'FB': 10.75}
        # 最低
        min_price = min(zip(prices.values(), prices.items()))
        print(min_price)
        # 最高
        max_price = max(zip(prices.values(), prices.items()))
        print(max_price)

        a = {'x': 1, 'y': 2, 'z': 3}
        b = {'w': 10, 'x': 11, 'y': 2}
        # 字典的key支持常见集合操作，因为存储原理基本一致，hash
        print(a.keys() & b.keys())

    def question_11(self):
        """
        问题11：对切片或者索引
        使用可命名切片，即切片对象代替硬编码
        """
        recording = "..........100.................513.25............."
        SHARES = slice(10, 13, 2)
        PRICE = slice(30, 36)
        print(recording[SHARES])
        print(recording[PRICE])
        # 切片对象有一些属性
        print(SHARES.start)
        print(SHARES.stop)
        print(SHARES.step)

    def question_12(self):
        """
        问题12：找出序列出现最多的元素
        clooections.Counter的使用
        Counter对象提供任何可哈希对象序列作为输入，在底层实现中是一个字典，还支持各种数学运算
        """
        words = [
            'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
            'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
            'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
            'my', 'eyes', "you're", 'under'
        ]

        word_counts = Counter(words)
        top_three = word_counts.most_common(3)
        print(top_three)
        more_words = ['why', 'are', 'you', 'not', 'look', 'in', 'my', 'eyes']
        # 更新计数
        word_counts.update(more_words)
        top_three = word_counts.most_common(3)
        print(top_three)

    def question_13(self):
        """
        问题13：通过公共键对字典序列排序
        operator.itemgetter 底层为调用__getitem__()
        比起lambda表达式更快
        """
        rows = [
            {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
            {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
            {'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
            {'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
        ]

        rows_by_fname = sorted(rows, key=itemgetter('fname'))
        rows_by_uid = sorted(rows, key=itemgetter('uid', 'lname'))
        print(rows_by_fname)
        print(rows_by_uid)

    def question_15(self):
        """
        问题15：根据字段将记录分组
        itertools.groupby() 通过扫描序列找出相同key或者使用key参数如下，将其分组，返回一个迭代器
        每次迭代都会返回字段value和一个子迭代器（所有该分组内的项）
        """
        rows = [
            {'address': '5412 N CLARK', 'date': '07/01/2012'},
            {'address': '5148 N CLARK', 'date': '07/04/2012'},
            {'address': '5800 E 58TH', 'date': '07/02/2012'},
            {'address': '2122 N CLARK', 'date': '07/03/2012'},
            {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
            {'address': '1060 W ADDISON', 'date': '07/02/2012'},
            {'address': '4801 N BROADWAY', 'date': '07/01/2012'},
            {'address': '1039 W GRANVILLE', 'date': '07/04/2012'},
        ]

        rows.sort(key=itemgetter('date'))
        for date, items in groupby(rows, key=itemgetter('date')):
            print(date)
            for i in items:
                print(' {}'.format(i))

    def question_20(self):
        """
        问题20：将多个映射合并为单个映射（逻辑上）
        接收多个映射然后再逻辑上使它们表现为一个单独的映射，chainmap维护一个记录底层映射的关系列表
        若有重复的键总是使用第一个映射结构
        """
        a = {'x': 1, 'z': 3}
        b = {'y': 2, 'z': 4}
        c = ChainMap(a, b)
        print(c['x'])
        print(c['y'])
        print(c['z'])


if __name__ == '__main__':
    solution = Solution()
    solution.question_1()
    solution.question_3()
    solution.question_4()
    solution.question_5()
    solution.question_6()
    solution.question_7()
    solution.question_11()
    solution.question_12()
    solution.question_13()
    solution.question_15()
    solution.question_20()
