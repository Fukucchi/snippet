class SegmentTree(object):
    # https://atcoder.jp/contests/abc014/submissions/3935971
    __slots__ = ["elem_size", "tree", "default", "op"]
    def __init__(self, a: list, default: int, op):
        from math import ceil, log
        real_size = len(a)
        self.elem_size = elem_size = 1 << ceil(log(real_size, 2))
        self.tree = tree = [default] * (elem_size * 2)
        tree[elem_size:elem_size + real_size] = a
        self.default = default
        self.op = op
        for i in range(elem_size - 1, 0, -1):
            tree[i] = op(tree[i << 1], tree[(i << 1) + 1])

    def get_value(self, x: int, y: int) -> int:  # 半開区間
        l, r = x + self.elem_size, y + self.elem_size
        tree, result, op = self.tree, self.default, self.op
        while l < r:
            if l & 1:
                result = op(tree[l], result)
                l += 1
            if r & 1:
                r -= 1
                result = op(tree[r], result)
            l, r = l >> 1, r >> 1
        return result

    def set_value(self, i: int, value: int) -> None:
        k = self.elem_size + i
        self.tree[k] = value
        self.update(k)

    def update(self, i: int) -> None:
        op, tree = self.op, self.tree
        while i > 1:
            i >>= 1
            tree[i] = op(tree[i << 1], tree[(i << 1) + 1])


class SegTreeIndex(object):
    # 区間の最小 or 最大値とその index を取得
    # 未検証
    __slots__ = ["elem_size", "tree", "default", "op", "index", "op2"]
    def __init__(self, a: list, default=float("inf"), op=min, op2=lambda a,b:a>b):
        # 同じ場合最左のインデックスを返す
        # 最大値・最左 -> -float("inf"), max, lambda a,b:a<=b
        from math import ceil, log
        real_size = len(a)
        self.elem_size = elem_size = 1 << ceil(log(real_size, 2))
        self.tree = tree = [default] * (elem_size * 2)
        self.index = index = [0] * (elem_size * 2)
        tree[elem_size:elem_size + real_size] = a
        index[elem_size:elem_size + real_size] = list(range(real_size))
        self.default = default
        self.op = op
        self.op2 = op2
        for i in range(elem_size-1, 0, -1):
            v1, v2 = tree[i<<1], tree[(i<<1)+1]
            tree[i] = op(v1, v2)
            index[i] = index[(i<<1) + op2(v1, v2)]

    def get_value(self, x: int, y: int) -> tuple:  # 半開区間
        l, r = x + self.elem_size, y + self.elem_size
        tree, result, op, op2, index = self.tree, self.default, self.op, self.op2, self.index
        idx = -1
        while l < r:
            if l & 1:
                v1, v2 = result, tree[l]
                result = op(v1, v2)
                if op2(v1, v2)==1:
                    idx = index[l]
                l += 1
            if r & 1:
                r -= 1
                v1, v2 = tree[r], result
                result = op(v1, v2)
                if op2(v1, v2)==0:
                    idx = index[l]
            l, r = l >> 1, r >> 1
        return result, idx

    def set_value(self, i: int, value: int) -> None:
        k = self.elem_size + i
        self.tree[k] = value
        self.update(k)

    def update(self, i: int) -> None:
        op, tree, index, op2 = self.op, self.tree, self.index, self.op2
        while i > 1:
            i >>= 1
            v1, v2 = tree[i<<1], tree[(i<<1)+1]
            tree[i] = op(v1, v2)
            index[i] = index[(i<<1) + op2(v1, v2)]


class SegTree(object):
    # 区間の中で v 以下の値のうち最も左にある値と index を取得
    # 普通のセグ木に get_threshold_left を加えただけ
    # 検証: https://atcoder.jp/contests/arc038/submissions/6933949 (全区間のみ)
    # 抽象化したい
    __slots__ = ["elem_size", "tree", "default", "op"]
    def __init__(self, a: list, default=float("inf"), op=min):
        from math import ceil, log
        real_size = len(a)
        self.elem_size = elem_size = 1 << ceil(log(real_size, 2))
        self.tree = tree = [default] * (elem_size * 2)
        tree[elem_size:elem_size + real_size] = a
        self.default = default
        self.op = op
        for i in range(elem_size - 1, 0, -1):
            tree[i] = op(tree[i << 1], tree[(i << 1) + 1])

    def get_value(self, x: int, y: int) -> int:  # 半開区間
        l, r = x + self.elem_size, y + self.elem_size
        tree, result, op = self.tree, self.default, self.op
        while l < r:
            if l & 1:
                result = op(tree[l], result)
                l += 1
            if r & 1:
                r -= 1
                result = op(tree[r], result)
            l, r = l >> 1, r >> 1
        return result

    def get_threshold_left(self, x, y, v):
        # v 以下の値
        tree, result, op, elem_size = self.tree, self.default, self.op, self.elem_size
        l, r = x + elem_size, y + elem_size
        idx_left = idx_right = -1  # 内部 index
        while l < r:
            if l & 1:
                result = op(tree[l], result)
                if idx_left == -1 and tree[l] <= v:
                    idx_left = l
                l += 1
            if r & 1:
                r -= 1
                result = op(tree[r], result)
                if tree[r] <= v:
                    idx_right = r
            l, r = l >> 1, r >> 1
        if idx_left==idx_right==-1:
            return -1, -1
        idx = idx_left if idx_left!=-1 else idx_right
        while idx < elem_size:
            idx <<= 1
            if tree[idx] > v:
                idx += 1
        return tree[idx], idx-elem_size

    def set_value(self, i: int, value: int) -> None:
        k = self.elem_size + i
        self.tree[k] = value
        self.update(k)

    def update(self, i: int) -> None:
        op, tree = self.op, self.tree
        while i > 1:
            i >>= 1
            tree[i] = op(tree[i << 1], tree[(i << 1) + 1])
