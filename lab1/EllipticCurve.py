from Point import Point
import math
import random
from common import *


class ElliptiCurve:
    def __init__(self, p, a, b, n) -> None:
        self.__p = p
        self.__a = a
        self.__b = b
        self.__n = n
        self.__infinity = Point(None, None)
        self.__infinity_projective = Point(0, 1, 0)

    
    @property
    def p(self) -> int:
        return self.__p


    @property
    def a(self) -> int:
        return self.__a

    
    @property
    def b(self) -> int:
        return self.__b

    
    @property
    def n(self) -> int:
        return self.__n

    
    @property
    def infinity(self) -> Point:
        return self.__infinity

    
    @property
    def infinity_projective(self) -> Point:
        return self.__infinity_projective

    
    def is_on_curve(self, p: Point) -> bool:
        x, y = p.x, p.y
        if x == None and y == None:
            return True
        else:
            return (y ** 2) % self.__p == (x ** 3 + self.__a * x + self.__b) % self.__p


    def to_projective(self, p: Point) -> Point:
        if p == self.infinity:
            return self.__infinity_projective
        else:
            return Point(p.x, p.y, 1)

    
    def to_affine(self, p: Point) -> Point:
        if p == self.__infinity_projective:
            return self.__infinity
        if p.z == None:
            return p
        return Point((p.x * inv(p.z, self.__p)) % self.__p, (p.y * inv(p.z, self.__p)) % self.__p)


    def PointDouble(self, p: Point) -> Point:
        if p.y == 0 or p == self.__infinity_projective:
            return self.__infinity_projective
        W = (self.__a * p.z ** 2 + 3 * p.x ** 2) % self.__p
        S = (p.y * p.z) % self.__p
        B = (p.x * p.y * S) % self.__p
        H = (W ** 2 - 8 * B) % self.__p
        X = 2 * H * S
        Y = W * (4 * B - H) - 8 * p.y ** 2 * S ** 2
        Z = 8 * S ** 3
        return Point(X % self.__p, Y % self.__p, Z % self.__p)


    def PointAdd(self, a: Point, b: Point) -> Point:
        if a == self.__infinity_projective:
            return b
        elif b == self.__infinity_projective:
            return a
        U1 = (b.y * a.z) % self.__p
        U2 = (a.y * b.z) % self.__p
        V1 = (b.x * a.z) % self.__p
        V2 = (a.x * b.z) % self.__p
        if V1 == V2:
            if U1 != U2:
                return self.__infinity_projective
            else:
                return self.PointDouble(a)
        U = (U1 - U2) % self.__p
        V = (V1 - V2) % self.__p
        W = (a.z * b.z) % self.__p
        A = (U ** 2 * W - V ** 3 - 2 * V ** 2 * V2) % self.__p
        X3 = (V * A) % self.__p
        Y3 = (U * (V ** 2 * V2 - A) - V ** 3 * U2) % self.__p
        Z3 = (V ** 3 * W) % self.__p
        return Point(X3, Y3, Z3)


    def ScalarMultiplication(self, k: int, p: Point) -> Point:
        q = self.__infinity_projective
        while k > 0:
            if k & 1 == 1:
                q = self.PointAdd(q, p)
            p = self.PointDouble(p)
            k >>= 1
        return q


    def ScalarMultiplicationMontgomery(self, k: int, p: Point) -> Point:
        R0 = self.__infinity_projective
        R1 = p
        # print(math.ceil(math.log2(k + 1)))
        l = math.ceil(math.log2(k + 1))
        for i in range(l + 1):
            if (k >> (l - i)) & 1 == 0:
                R1 = self.PointAdd(R0, R1)
                R0 = self.PointDouble(R0)
            else:
                R0 = self.PointAdd(R1, R0)
                R1 = self.PointDouble(R1)
        return Point(R0.x % self.__p, R0.y % self.__p, R0.z % self.__p)


    def get_random_aff_point(self) -> Point:
        temp = Point(-1, -1)
        while not self.is_on_curve(temp):
            x = random.randint(1, self.__p)
            print(x)
            y = sqrt_mod((x ** 3 + self.__a * x + self.__b) % self.__p, self.__p)
            temp = Point(x, y)
        return temp


# 224 не работает
# p = 0xffffffffffffffffffffffffffffffff000000000000000000000001
# a = 0xfffffffffffffffffffffffffffffffefffffffffffffffffffffffe
# b = 0xb4050a850c04b3abf54132565044b0b7d7bfd8ba270b39432355ffb4
# n = 0xffffffffffffffffffffffffffff16a2e0b8f03e13dd29455c5c2a3d

# 192
# p = 0xfffffffffffffffffffffffffffffffeffffffffffffffff
# a = 0xfffffffffffffffffffffffffffffffefffffffffffffffc
# b = 0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1
# n = 0xffffffffffffffffffffffff99def836146bc9b1b4d22831

# 256
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551

ec = ElliptiCurve(p, a, b, n)

# print(ec.is_on_curve(A))

# Apr = ec.to_projective(A)

# Adouble = ec.PointDouble(Apr)
# Aadd = ec.PointAdd(Apr, Apr)

# Aaf = ec.to_affine(Aadd)

# print(Adouble)
# print(Aadd)
# print(ec.is_on_curve(Aaf))


B = ec.get_random_aff_point()

B = ec.to_projective(B)

Bscal = ec.ScalarMultiplication(n, B)

print('Bscal')
print(Bscal)
print(ec.is_on_curve(Bscal))
BMont = ec.ScalarMultiplicationMontgomery(n, B)
print(BMont)
print(ec.is_on_curve(BMont))

print(Bscal == BMont)