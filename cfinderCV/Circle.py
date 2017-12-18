class Circle:

    def __init__(self, x: int, y: int, radius: int):
        self._x = x
        self._y = y
        self._radius = radius

    def __str__(self) -> str:
        return "[Circle] x=%d, y=%s, radius=%s" % (self._x, self._y, self._radius)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def radius(self):
        return self._radius
