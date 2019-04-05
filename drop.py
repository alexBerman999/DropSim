import scipy, numpy
import matplotlib.pyplot as plt

CD = 0.5
RHO = 1.2
A = 0.37
D = 0.5 * CD * RHO * A
M = 0.267
G = 9.81
DT = 0.005

def distance_down_range(v, h):
    x = [0]
    y = [h]
    theta = 0
    vx = v * numpy.cos(theta)
    vy = v * numpy.sin(theta)
    i = 1
    ax = ((-1 * D)/M) * vx * (((vx**2) + (vy**2))**0.5)
    ay = (((-1 * D)/M) * vy * (((vx**2) + (vy**2))**0.5)) - G
    time = 0
    while min(y) >= 0:
        vx = vx + (ax * DT)
        vy = vy + (ay * DT)
        ax = ((-1 * D)/M) * vx * (((vx**2) + (vy**2))**0.5)
        ay = (((-1 * D)/M) * vy * (((vx**2) + (vy**2))**0.5)) - G
        x.append(x[i-1] + (vx * DT))
        y.append(y[i-1] + (vy * DT))
        i = i + 1
        time = time + DT
    print(time)
    return [x, y]

axis = distance_down_range(18, 45)
plt.plot(axis[0], axis[1])
plt.show()
