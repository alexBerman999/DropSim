import numpy
import matplotlib.pyplot as plot

#Unit Conversions
    """
        Converts degrees latitude to meters. This conversion finds the east/west
        distance in meters between the supplied point and origin. The Origin is
        a list in the format [latitude, longitude]
    """
    def degreesLatToMeters(origin, degrees):
        latR = math.radians(origin[0])
        return (degrees - origin[0]) * (111132.954 - (559.822 * math.cos(2 * latR)) +	(1.175 * math.cos(4 * latR)) - (0.0023 * math.cos(6 * latR)))

    """
        Converts degrees longitude to meters. This conversion finds the
        north/south distance in meters between the supplied point and origin.
        The Origin is a list in the format [latitude, longitude]
    """
    def degreesLongToMeters(origin, degrees):
        latR = math.radians(origin[0])
        return (degrees - origin[1]) * (111132.954 * math.cos(latR))

    """
        Converts meters to degrees latitude. This conversion finds the point
        meters to the east/west of the origin. The Origin is a list in the format [latitude, longitude]
    """
    def metersToDegreesLat(origin, meters):
	    latR = math.radians(origin[0])
	    return (meters / (111132.954 - (559.822 * math.cos(2 * latR)) + (1.175 * math.cos(4 * latR)) - (0.0023 * math.cos(6 * latR)))) + origin[0]

    """
        Converts meters to degrees longitude. This conversion finds the point
        meters to the north/south of the origin. The Origin is a list in the format [latitude, longitude]
    """
    def metersToDegreesLong(origin, meters):
        latR = math.radians(origin[0])
        return (meters / (111132.954 * math.cos(latR))) + origin[1]


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
    return [x, y]

axis = distance_down_range(18, 45, 3)
#Printing landing point
print("X: " + str(axis[0][-1]) + "m\tY: " + str(axis[1][-1]) + "m")
plot.plot(axis[0], axis[1])
plot.xlabel("Down Range Distance (Meters)")
plot.ylabel("Altitude (Meters)")
plot.title("Drop Path")
plot.show()
