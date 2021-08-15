## Output data:
# Area: A
# Second moments of area: Ix, Iy
# Product moment of area: Ixy
# Section moduli: Kx, Ky
# (Plus in case of circularly symmetric cross-section:
#   Polar moment of area: Ip
#   Polar modulus: Kp)
import numpy as np

def Circle(d,i_d=0):
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
    return properties

def Rectangle(w, h, i_W=0, i_h=0):
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
    return properties


def RectangularHS(w1, h1, w2, h2):
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

def Ellipse(a, b, i_a=0, i_b=0):
    A = a/2 * b/2 * np.pi
    Ix = a/2 * (b/2) ** 3 * np.pi / 4
    Iy = (a/2) ** 3 * b/2 * np.pi / 4
    Ixy = 0
    Kx = Ix / (b/2)
    Ky = Iy / (a/2)
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

def IsoscelesTriangle(w, h, i_w=0, i_h=0):
    A = w * h / 2
    Ix = w * h ** 3 / 36
    Iy = w ** 3 * h / 48
    Ixy = 0
    Kx = 3 * Ix / 2 / h
    Ky = 2 * Iy / w
    if Iy > Ix:
        alpha = np.pi/2
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