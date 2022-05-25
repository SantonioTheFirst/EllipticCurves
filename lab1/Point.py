class Point:
    def __init__(self, x, y, z=None):
        self.x = x
        self.y = y
        self.z = z


    def __str__(self):
        s = f'Point\n\tx = {hex(self.x)}\n\ty = {hex(self.y)}\n\tz = {hex(self.z)}\n' if self.z != None else\
            f'Point\n\tx = {hex(self.x)}\n\ty = {hex(self.y)}\n'
        return s

    
    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y and self.z == __o.z