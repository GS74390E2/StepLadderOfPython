"""
struct 模块提供了一些函数，把打包的字节序列转换成不同类型字段组成的元组，还有
一些函数用于执行反向转换，把元组转换成打包的字节序列。struct 模块能处理 bytes、
bytearray 和 memoryview 对象

格式字符

格式字符有下面的定义：

Format	          C Type	        Python	            字节数
    x	        pad byte	        no value	        1
    c	        char	        bytes of length 1	    1
    b	        signed char	        integer	            1
    B	        unsigned char	    integer	            1
    ？	        _Bool	            bool	            1
    h           short               integer	            2
    H	        unsigned short	    integer	            2
    i	        int	                integer	            4
    I	        unsigned int	    integer	            4
    l	        long	            integer	            4
    L	        unsigned long	    integer	            4
    q	        long long	        integer	            8
    Q	        unsigned long long	integer	            8
    f	        float	            float	            4
    d	        double	            float	            8
    s	        char[]	            bytes	            1
    p	        char[]	            bytes	            1
    P	        void *	            integer

"""
import struct

# unsigned char 、 char[4] 、 2个unsigned int
# 将以上四种类型打包成一个bytes二进制串
s = 'names'.encode('utf-8')
a = struct.pack('B5sII', 0x04, s, 0x01, 0x0e)
print(type(a))
print(len(a))

# 拆包成元组
typ, tag, version, length = struct.unpack('B5sII', a)
print("type: {}".format(typ))
print("tag: {}".format(tag))
print("version: {}".format(version))
print("length: {}".format(length))

# 返回fmt的大小
print(struct.calcsize('B5sII'))