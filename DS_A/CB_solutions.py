from collections import deque
import heapq


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


if __name__ == '__main__':
    solution = Solution()
    # solution.question_1()
    # solution.question_3()
    solution.question_4()
