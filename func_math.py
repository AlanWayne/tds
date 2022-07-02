import math

# calculate distance between objects
def distance_to_object(a,b):
    return ( math.sqrt ( pow ( ( b.x - a.x ) , 2 ) + pow ( ( b.y - a.y ) , 2 ) ) )

# calculate distance between object and point
def distance_to_point(a,x,y):
    return ( math.sqrt ( pow ( ( x - a.x   ) , 2 ) + pow ( ( y - a.y   ) , 2 ) ) )

# find distance between two points
def distance_between(a,b,x,y):
    return ( math.sqrt ( pow ( ( x - a     ) , 2 ) + pow ( ( y - b     ) , 2 ) ) )

# find velocity relative to direction
def relative_velocity(x1, y1, x2, y2):
    d_denominator = abs(x1 - x2) + abs(y1 - y2)
    if d_denominator == 0:
        return (0,0)
    else:
        dx = abs(x1 - x2) / d_denominator
        dy = abs(y1 - y2) / d_denominator
        return(dx,dy)