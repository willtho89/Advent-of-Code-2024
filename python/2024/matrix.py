from collections import defaultdict


class Matrix:
    def __init__(self, size, default=0, wrap=False):
        self.size = size
        self.default = default
        self.wrap = wrap
        self.matrix = defaultdict(lambda: default)

    def _convert_pos(self, pos):
        out = []
        if self.wrap:
            for i, elem in enumerate(pos):
                out.append(str(elem % self.size[i]))
        else:
            out = list(map(str, pos))
        return ",".join(out)

    def set(self, pos, val):
        if len(pos) != len(self.size):
            raise Exception("Size of pos does not match initialized size.")
        if not self._is_in_bounds(pos):
            return None  # raise IndexError("Cannot SET outside bounds of matrix.")
        self.matrix[self._convert_pos(pos)] = val

    def get(self, pos):
        if len(pos) != len(self.size):
            raise Exception("Size of pos does not match initialized size.")
        if not self._is_in_bounds(pos):
            return None  # raise IndexError("Cannot GET outside bounds of matrix.")
        return self.matrix[self._convert_pos(pos)]

    def _is_in_bounds(self, pos):
        if not self.wrap:
            for i in range(len(self.size)):
                if pos[i] < 0 or pos[i] >= self.size[i]:
                    return False
        return True

    def __str__(self):
        out = []
        if len(self.size) == 1:
            for i in range(self.size[0]):
                out.append(str(self.matrix[f"{i}"]))
            return " ".join(out)
        elif len(self.size) == 2:
            for i in range(self.size[0]):
                temp = []
                for j in range(self.size[1]):
                    temp.append(str(self.matrix[f"{i},{j}"]))
                out.append(" ".join(temp))
            return "\n".join(out)
        else:
            raise IndexError("Dimensions do not support printing.")

    def __iter__(self):
        pos = [0 for _ in self.size]
        while pos != [x - 1 for x in self.size]:
            yield pos, self.get(pos)
            i = -1
            pos[i] += 1
            while True:
                if pos[i] == self.size[i]:
                    pos[i] = 0
                    i -= 1
                    pos[i] += 1
                else:
                    break
        yield pos, self.get(pos)

    def __setitem__(self, key, value):
        self.set(list(key), value)

    def __getitem__(self, item):
        return self.get(list(item))

    def neighbors(self, pos, diag=False):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (not diag and abs(i + j) == 1) or (diag and not (i == 0 and j == 0)):
                    got = self.get([pos[0] + i, pos[1] + j])
                    if got is not None:
                        yield got, [pos[0] + i, pos[1] + j]
