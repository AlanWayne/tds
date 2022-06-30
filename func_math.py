import math

def distance_to_object(a,b):
    return ( math.sqrt ( pow ( ( b.x - a.x ) , 2 ) + pow ( ( b.y - a.y ) , 2 ) ) )

def distance_to_point(a,x,y):
    return ( math.sqrt ( pow ( ( x - a.x   ) , 2 ) + pow ( ( y - a.y   ) , 2 ) ) )

def distance_between(a,b,x,y):
    return ( math.sqrt ( pow ( ( x - a     ) , 2 ) + pow ( ( y - b     ) , 2 ) ) )

def find_nearest(a,list):
    d = a
    for b in list:
        if d == a:
            d = b
        if distance_to_object(a,b) < distance_to_object(a,d):
            d = b
    return d

def find_nearest_brother(a,list):
    d = a
    for b in list:
        if b != a:
            if d == a:
                d = b
            if distance_to_object(a,b) < distance_to_object(a,d):
                d = b
    if d == a:
        return 0
    else:
        return d
    
def relative_velocity(x1, y1, x2, y2):
    d_denominator = abs(x1 - x2) + abs(y1 - y2)
    if d_denominator == 0:
        return (0,0)
    else:
        dx = abs(x1 - x2) / d_denominator
        dy = abs(y1 - y2) / d_denominator
        return(dx,dy)