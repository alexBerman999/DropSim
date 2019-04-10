import numpy
import matplotlib.pyplot as plt

CD = 0.5
RHO = 1.2
A = 0.37
D = 0.5 * CD * RHO * A
M = 0.267
G = 9.81
DT = 0.005

"""
    Calculates the down-range distance in meters
    of an object described by the above parameters
    traveling at velocity v (m/s), at height h (m) in
    an environment with tail wind tail_wind (m/s). This
    will not account for crosswinds and assumes a constant
    windspeed. It is further assumed the object is travelling
    horizontally.
"""
def distance_down_range(v, h, tail_wind):
    x = [0]
    y = [h]
    #This assumes the object is travelling horizontally.
    theta = 0
    vx = v * numpy.cos(theta)
    vy = v * numpy.sin(theta)
    i = 1
    ax = (D/M) * tail_wind**2 + ((-1 * D)/M) * vx * (((vx**2) + (vy**2))**0.5)
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

axis = distance_down_range(18, 45, 3)
#Printing landing point
print("X: " + str(axis[0][-1]) + "m\tY: " + str(axis[1][-1]) + "m")
plt.plot(axis[0], axis[1])
plt.xlabel("Down Range Distance (Meters)")
plt.ylabel("Altitude (Meters)")
plt.title("Drop Path")
plt.show()
