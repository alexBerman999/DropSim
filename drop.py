import sys
import numpy
import matplotlib.pyplot as plot

#Unit Conversions
"""
    Converts degrees latitude to meters. This conversion finds the east/west
    distance in meters between the supplied point and origin. The Origin is
    a list in the format [latitude, longitude]
"""
def degreesLatToMeters(origin, degrees):
    latR = numpy.deg2rad(origin[0])
    return (degrees - origin[0]) * (111132.954 - (559.822 * numpy.cos(2 * latR)) +	(1.175 * numpy.cos(4 * latR)) - (0.0023 * numpy.cos(6 * latR)))

"""
    Converts degrees longitude to meters. This conversion finds the
    north/south distance in meters between the supplied point and origin.
    The Origin is a list in the format [latitude, longitude]
"""
def degreesLongToMeters(origin, degrees):
    latR = numpy.deg2rad(origin[0])
    return (degrees - origin[1]) * (111132.954 * numpy.cos(latR))

"""
    Converts meters to degrees latitude. This conversion finds the point
    meters to the east/west of the origin. The Origin is a list in the format [latitude, longitude]
"""
def metersToDegreesLat(origin, meters):
    latR = numpy.deg2rad(origin[0])
    return (meters / (111132.954 - (559.822 * numpy.cos(2 * latR)) + (1.175 * numpy.cos(4 * latR)) - (0.0023 * numpy.cos(6 * latR)))) + origin[0]

"""
    Converts meters to degrees longitude. This conversion finds the point
    meters to the north/south of the origin. The Origin is a list in the format [latitude, longitude]
"""
def metersToDegreesLong(origin, meters):
    latR = numpy.deg2rad(origin[0])
    return (meters / (111132.954 * numpy.cos(latR))) + origin[1]


CD = 0.5
RHO = 1.2
A = 0.37
D = 0.5 * CD * RHO * A
M = 0.267
G = 9.81
DT = 0.005

INITIAL_SPEED = 18
INITIAL_HEIGHT = 45

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

if len(sys.argv) == 2:
    if sys.argv[1] == "-h" or sys.argv[1] == "help":
        print("""\tpython3 drop.py float target_latitude float target_longitude
\tfloat wind_direction float wind_speed Latitude and longitude
\tare in degrees North East (meaning west and south are
\trepresented by negative numbers). Wind direction is provided
\tin degrees with North as 0 degrees. Wind speed is provided in
\tmeters per second. The returned values are the degrees latitude
\tand degrees longitude the payload is to be dropped at to land
\tat the target coordinate.""")
    elif sys.argv[1] == "-a":
        print("""\tAssumptions:
\t\tCoefficient of Drag = {}
\t\tDensity = {}kg/m^2
\t\tArea = {}m^2
\t\tMass = {}kg
\t\tGravity = {}m/s^2
\t\tTime Step = {}s
\t\tInitial Airspeed = {}m/s
\t\tInitial Height = {}m""".format(CD, RHO, A, M, G, DT, INITIAL_SPEED, INITIAL_HEIGHT))

elif len(sys.argv) != 5:
    print("Invalid number of arguments. " + str(len(sys.argv) - 1) + " provided\
    when 4 were required")
else:
    target = [float(sys.argv[1]), float(sys.argv[2])]
    wind_direction = float(sys.argv[3])
    wind_speed = float(sys.argv[4])

    axis = distance_down_range(INITIAL_SPEED, INITIAL_HEIGHT, wind_speed)
    distance = axis[0][-1]
    drop_point = [0, 0]
    drop_point[0] -= distance * numpy.cos(numpy.deg2rad(wind_direction))
    drop_point[1] -= distance * numpy.sin(numpy.deg2rad(wind_direction))
    drop_coords = [metersToDegreesLat(target, drop_point[1]), metersToDegreesLong(target, drop_point[0])]
    print(str(drop_coords[0]) + " " + str(drop_coords[1]))

    plot.plot(axis[0], axis[1])
    plot.xlabel("Down Range Distance (Meters)")
    plot.ylabel("Altitude (Meters)")
    plot.title("Drop Path")
    plot.show()
