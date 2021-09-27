## Output data:
# Area: A
# Second moments of area: Ix, Iy
# Product moment of area: Ixy
# Section moduli: Kx, Ky
# (Plus in case of circularly symmetric cross-section:
#   Polar moment of area: Ip
#   Polar modulus: Kp)
import numpy as np
import math
def transform(func):
    def inner(*args, **kwargs):
        if len(args) >3:
            ans = func(*args[:-3])
            if not kwargs['rad']: #conversion if the default unit isnt radian
                phi= math.radians(args[-1])
            else:
                phi = args[-1]
            ans["Ix"], ans["Iy"], ans["Ixy"] = Iarbitraryaxis(**ans, x=args[-3],y=args[-2], phi=phi)
            
        else:
            ans = func(*args)
        return ans
    return inner

@transform
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

@transform
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
        properties = RectangularHS(w, h, w-2*t, h-2*t)
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

@transform
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

@transform
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
    else:
        w2 = w
        h2 = h
        # w1 = w - t # HIBA # itt a falvastagság értelmezése nem helyes, ezt javítva
        # h1 = h - t
        phi = np.arctan(h / (w / 2))
        u = t / np.sin(phi)
        v = t / np.tan(phi)
        w1 = w - 2 * (u + v)
        h1 = h * (w1 / w)
        A = (w2 * h2 - w1 * h1) / 2
        Ix = (w2 * h2 ** 3 - w1 * h1 ** 3) / 36
        Iy = (w2 ** 3 * h2 - w1 ** 3 * h1) / 48
        Ixy = 0
        Kx = 3 * Ix / 2 / h2
        Ky = 2 * Iy / w2
        alpha = None #! CHECK!!!!
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

def Iarbitraryaxis(A, Ix, Iy, Ixy, x, y, phi, *args, **kwargs):
    Ix2 = Ix + x ** 2 * A 
    Iy2 = Iy + y ** 2 * A 
    Ix2y2 = Ixy + x * y * A
    Ixi = Ix2 * np.cos(phi) ** 2 + Iy2 * np.sin(phi) ** 2 - Ix2y2 * np.sin(2 * phi)
    Ieta = Ix2 * np.sin(phi) ** 2 + Iy2 * np.cos(phi) ** 2 + Ix2y2 * np.sin(2 * phi) # itt pedig az utolsó tagnak negatív volt az előjele, Kossa A. jegyzetében én pozitívan találtam
    # így szerepelt eredetileg: Ieta = Ix2 * np.sin(phi) ** 2 + Iy2 * np.cos(phi) ** 2 - Ix2y2 * np.sin(2 * phi)
    Ixieta = (Ix2 - Iy2) / 2 * np.sin(2 * phi) + Ix2y2 * np.cos(2 * phi)
    return Ixi, Ieta, Ixieta
