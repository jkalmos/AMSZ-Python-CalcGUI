## Output data:
# Area: A
# Second moments of area: Ix, Iy
# Product moment of area: Ixy
# Section moduli: Kx, Ky
# (Plus in case of circularly symmetric cross-section:
#   Polar moment of area: Ip
#   Polar modulus: Kp)
import numpy as np

def Circle(d):
    A = d ** 2 * np.pi / 4
    Ix = d ** 4 * np.pi / 64
    Iy = Ix
    Ixy = 0
    Kx = 2 * Ix / d
    Ky = Kx
    Ip = Ix + Iy
    Kp = 2 * Ip / d
    alpha = 0
    return A, Ix, Iy, Ixy, Kx, Ky, Ip, Kp, alpha

def Ring(d1, d2):
    A = (d2 ** 2 - d1 ** 2) * np.pi / 4
    Ix = (d2 ** 4 - d1 ** 4) * np.pi / 64
    Iy = Ix
    Ixy = 0
    Kx = 2 * Ix / d2
    Ky = Kx
    Ip = Ix + Iy
    Kp = 2 * Ip / d2
    alpha = 0
    return A, Ix, Iy, Ixy, Kx, Ky, Ip, Kp, alpha

def Rectangle(w, h):
    A = w * h
    Ix = w * h ** 3 / 12
    Iy = w ** 3 * h / 12
    Ixy =  0
    Kx = 2 * Ix / h
    Ky = 2 * Iy / w
    if Iy > Ix:
        alpha = np.pi / 2
    else:
        alpha = 0
    return A, Ix, Iy, Ixy, Kx, Ky, alpha

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
    return A, Ix, Iy, Ixy, Kx, Ky, alpha

def Ellipse(a, b):
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
    return A, Ix, Iy, Ixy, Kx, Ky, alpha

def IsoscelesTriangle(w, h):
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
    return A, Ix, Iy, Ixy, Kx, Ky, alpha