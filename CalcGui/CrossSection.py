## Output data:
# Area: A
# Second moments of area: Ix, Iy
# Product moment of area: Ixy
# Section moduli: Kx, Ky
# (Plus in case of circularly symmetric cross-section:
#   Polar moment of area: Ip
#   Polar modulus: Kp)
import numpy as np


def Circle(d, t = 0):
    if t == 0:
        properties = {
            "A": d ** 2 * np.pi / 4,
            "Ix": d ** 4 * np.pi / 64,
            "Iy": d ** 4 * np.pi / 64,
            "Ixy": 0,
            "Kx": d ** 3 * np.pi / 32,
            "Ky": d ** 3 * np.pi / 32,
            "Ip": d ** 4 * np.pi / 32,
            "Kp": d ** 3 * np.pi / 16,
            "alpha": 0,
        }
    else:
        di = d - t
        properties = {
            "A": (d ** 2 - di ** 2) * np.pi / 4,
            "Ix": (d ** 4 - di ** 4) * np.pi / 64,
            "Iy": (d ** 4 - di ** 4) * np.pi / 64,
            "Ixy": 0,
            "Kx": (d ** 4 - di ** 4) * np.pi / (32 * d),
            "Ky": (d ** 4 - di ** 4) * np.pi / (32 * d),
            "Ip": (d ** 4 - di ** 4) * np.pi / 32,
            "Kp": (d ** 4 - di ** 4) * np.pi / (16 * d),
            "alpha": 0,
        }
    return properties


def Ring(d2, d1):
    properties = {
        "A": (d2 ** 2 - d1 ** 2) * np.pi / 4,
        "Ix": (d2 ** 4 - d1 ** 4) * np.pi / 64,
        "Iy": (d2 ** 4 - d1 ** 4) * np.pi / 64,
        "Ixy": 0,
        "Kx": (d2 ** 3 - d1 ** 3) * np.pi / (32 * d2),
        "Ky": (d2 ** 3 - d1 ** 3) * np.pi / (32 * d2),
        "Ip": (d2 ** 4 - d1 ** 4) * np.pi / 32,
        "Kp": (d2 ** 4 - d1 ** 4) * np.pi / (16 * d2),
        "alpha": 0,
    }
    return properties


def Rectangle(w, h, t = 0):
    if t == 0:
        A = w * h
        Ix = w * h ** 3 / 12
        Iy = w ** 3 * h / 12
        Ixy = 0
        Kx = 2 * Ix / h
        Ky = 2 * Iy / w
        if Iy > Ix:
            alpha = np.pi / 2
        else:
            alpha = 0

        properties = {
            "A": A,
            "Ix": Ix,
            "Iy": Iy,
            "Ixy": Ixy,
            "Kx": Kx,
            "Ky": Ky,
            "alpha": alpha,
        }
    else:
        properties = RectangularHS(w, h, w-t, h-t)
    return properties


def RectangularHS(w2, h2, w1, h1):
    A = (w2 * h2) - (w1 * h1)
    Ix = (w2 * h2 ** 3 - w1 * h1 ** 3) / 12
    Iy = (w2 ** 3 * h2 - w1 ** 3 * h1) / 12
    Ixy = 0
    Kx = 2 * Ix / h2
    Ky = 2 * Iy / w2
    if Iy > Ix:
        alpha = np.pi / 2
    else:
        alpha = 0

    properties = {
        "A": A,
        "Ix": Ix,
        "Iy": Iy,
        "Ixy": Ixy,
        "Kx": Kx,
        "Ky": Ky,
        "alpha": alpha,
    }
    return properties


def Ellipse(a, b, t = 0):
    if t == 0:
        A = a * b * np.pi
        Ix = a * b ** 3 * np.pi / 4
        Iy = a ** 3 * b * np.pi / 4
        Ixy = 0
        Kx = Ix / b
        Ky = Iy / a
        if Iy > Ix:
            alpha = np.pi / 2
        else:
            alpha = 0

        properties = {
            "A": A,
            "Ix": Ix,
            "Iy": Iy,
            "Ixy": Ixy,
            "Kx": Kx,
            "Ky": Ky,
            "alpha": alpha,
        }
    else:
        a2 = a
        b2 = b
        a1 = a - t
        b1 = b - t
        A = (a2 * b2 - a1 * b1) * np.pi
        Ix = (a2 * b2 ** 3 - a1 * b1 ** 3) * np.pi / 4
        Iy = (a2 ** 3 * b2 - a1 ** 3 * b1) * np.pi / 4
        Ixy = 0
        Kx = Ix / b2
        Ky = Iy / a2
        if Iy > Ix:
            alpha = np.pi / 2
        else:
            alpha = 0

        properties = {
            "A": A,
            "Ix": Ix,
            "Iy": Iy,
            "Ixy": Ixy,
            "Kx": Kx,
            "Ky": Ky,
            "alpha": alpha,
        }
    return properties


def IsoscelesTriangle(w, h, t = 0):
    if t == 0:
        A = w * h / 2
        Ix = w * h ** 3 / 36
        Iy = w ** 3 * h / 48
        Ixy = 0
        Kx = 3 * Ix / 2 / h
        Ky = 2 * Iy / w
        if Iy > Ix:
            alpha = np.pi / 2
        else:
            alpha = 0

        properties = {
            "A": A,
            "Ix": Ix,
            "Iy": Iy,
            "Ixy": Ixy,
            "Kx": Kx,
            "Ky": Ky,
            "alpha": alpha,
        }
    else:
        w2 = w
        h2 = h
        w1 = w - t
        h1 = h - t
        A = (w2 * h2 - w1 * h1) / 2
        Ix = (w2 * h2 ** 3 - w1 * h1 ** 3) / 36
        Iy = (w2 ** 3 * h2 - w1 ** 3 * h1) / 48
        Ixy = 0
        Kx = 3 * Ix / 2 / h2
        Ky = 2 * Iy / w2
    return properties

def Iarbitraryaxis(A, Ix, Iy, Ixy, x, y, alpha):
    Ix2 = Ix + y ** 2 * A
    Iy2 = Iy + x ** 2 * A
    Ix2y2 = Ixy + x * y * A
    Ixi = Ix2 * np.cos(alpha) ** 2 + Iy2 * np.sin(alpha) ** 2 - Ix2y2 * np.sin(2 * alpha)
    Ieta = Ix2 * np.sin(alpha) ** 2 + Iy2 * np.cos(alpha) ** 2 - Ix2y2 * np.sin(2 * alpha)
    Ixieta = (Ix2 - Iy2) / 2 * np.sin(2 * alpha) + Ix2y2 * np.cos(2 * alpha)
    return Ixi, Ieta, Ixieta
