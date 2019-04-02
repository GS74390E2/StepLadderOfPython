"""
python标准库——array，数组
The following type codes are defined:

    Type code   C Type             Minimum size in bytes
    'b'         signed integer     1
    'B'         unsigned integer   1
    'u'         Unicode character  2 (see note)
    'h'         signed integer     2
    'H'         unsigned integer   2
    'i'         signed integer     2
    'I'         unsigned integer   2
    'l'         signed integer     4
    'L'         unsigned integer   4
    'q'         signed integer     8 (see note)
    'Q'         unsigned integer   8 (see note)
    'f'         floating point     4
    'd'         floating point     8

Methods:

    append() -- append a new item to the end of the array
    buffer_info() -- return information giving the current memory info
    byteswap() -- byteswap all the items of the array
    count() -- return number of occurrences of an object
    extend() -- extend array by appending multiple elements from an iterable
    fromfile() -- read items from a file object
    fromlist() -- append items from the list
    frombytes() -- append items from the string
    index() -- return index of first occurrence of an object
    insert() -- insert a new item into the array at a provided position
    pop() -- remove and return item (default last)
    remove() -- remove first occurrence of an object
    reverse() -- reverse the order of the items in the array
    tofile() -- write all items to a file object
    tolist() -- return the array converted to an ordinary list
    tobytes() -- return the array converted to a string
"""
from array import array


def main():
    # 参数1：指定数组元素类型，对应c语言类型
    # 参数2：可迭代对象
    arr = array('i', (i for i in range(10 ** 7)))
    print(arr.buffer_info())
    # 文件操作
    fd = open('./floats.bin', 'wb')
    print(arr[-1])
    arr.tofile(fd)
    fd.close()

    floats2 = array('i')
    fd = open('./floats.bin', 'rb')
    floats2.fromfile(fd, 10 ** 7)
    print(floats2[-1])
    fd.close()


if __name__ == '__main__':
    main()
