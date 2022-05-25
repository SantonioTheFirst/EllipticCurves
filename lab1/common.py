def extgcd(a: int, b: int) -> tuple:
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    return (old_s, old_t, old_r)


def sqrt_mod(a, p):
    k = (p - 3) >> 2
    return pow(a, k + 1, p)


def inv(a: int, p: int) -> int:
    s, t, g = extgcd(a, p)
    return s % p if g == 1 else None