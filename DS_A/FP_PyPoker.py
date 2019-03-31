from collections import namedtuple
from random import choice
from sys import exit


# 扑克牌，数据结构选用可命名元组，rank代表牌面值，suit代表花色
Card = namedtuple('Card', ['rank', 'suit'])


# 可命名元组的第二个参数必须是一个可迭代对象（若是一个字符串支持两种方式：不同name用空格分割；用逗号分割，详情可见文档）
# nametuple初始化时会做类型转换，obj -> str -> list
n1 = namedtuple("n1", "x,y")
n2 = namedtuple("n2", "x y")
# 可以使用.操作符操作属性
print(n1.x)
print(n2.y)
# 显示所有字段
print(n1._fields)
# 可以转化为collections.orderedDict
point = (3, 4)
coordinate = n1._make(point)
print(coordinate)
print(coordinate._asdict())
exit(0)


class FrenchDeck:
    """
    扑克牌类
    """
    ranks = [str(i) for i in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self.cards = [Card(rank, suit) for rank in self.ranks for suit in self.suits]

    def __len__(self):
        """支持len()"""
        return len(self.cards)

    def __getitem__(self, item):
        """支持[]相应的下标运算、切片、迭代"""
        return self.cards[item]


suit_value = dict(spades=3, hearts=2, diamonds=1, clubs=0)


def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_value) + suit_value[card.suit]


def main():
    deck = FrenchDeck()
    print(len(deck))
    print(deck[0])
    print(deck[-1])

    # tips1: random.choice方法，从对象中随机取一个元素，要求对象必须有__len__()方法
    print(choice(deck))

    # tips2: 因为实现了__getitem__()，也支持切片操作
    print(deck[:3])
    print(deck[12:13])

    # tips3: 迭代通常是隐式的，因为实现了__getitem__()，支持迭代
    for card in deck:
        print(card)
    for card in reversed(deck):
        print(card)

    # tip4: in运算符在没有__conatins__()时，按顺序迭代搜索
    print(Card('Q', 'hearts') in deck)
    print(Card('7', 'beasts') in deck)
    for card in sorted(deck, key=spades_high):
        print(card)


if __name__ == '__main__':
    main()
