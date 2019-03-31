"""
disect模块: 包含两个主要函数，bisect 和 insort
两个函数都利用二分查找算法来在 有序 序列中查找或插入元素
"""
import bisect


HAYSTACK = [1, 4, 5, 6, 8, 12, 15, 20, 21, 23, 23, 26, 29, 30]
NEEDLES = [0, 1, 2, 5, 8, 10, 22, 23, 29, 30, 31]


def main():
    """查询
        bisect.bisect(haystack, needle): 从haystack(干草垛，一个有序的序列)查找needle(针)应该插入的位置
                    返回值是index，序列仍保持升序
        bisect.bisect_left: 返回的插入位置是原序列中被插入元素相等的元素位置
        bisect.bisect_right: 返回的是跟插入元素相等元素之后的位置
        插入
        bisect.insort(item, seq): 把变量插入到序列中，仍能保持seq的升序顺序
        等同于线bisect.bisect()找出插入位置，再insert到序列中，但insort更快
    """
    for needle in NEEDLES:
        index_v1 = bisect.bisect(HAYSTACK, needle)
        print(index_v1)
        index_v2 = bisect.bisect_left(HAYSTACK, needle)
        print(index_v2)
        index_v3 = bisect.bisect_right(HAYSTACK, needle)
        print(index_v3)
        bisect.insort(HAYSTACK, needle)
    print(HAYSTACK)


if __name__ == '__main__':
    main()
