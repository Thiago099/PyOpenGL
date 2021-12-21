import math

def subtract(v0, v1):
    return [v0[0]-v1[0], v0[1]-v1[1], v0[2]-v1[2]]
    
def dot(v0, v1):
    return v0[0]*v1[0]+v0[1]*v1[1]+v0[2]*v1[2]

def length(v):
    return math.sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2])

def normalize(v):
    l = length(v)
    return [v[0]/l, v[1]/l, v[2]/l]

def isectSphere(p0, p1, C, R):
    A = p0               # origin 
    B = normalize(subtract(p1, p0)) # direction
    oc = subtract(A, C) 
    a = dot(B, B)
    b = 2 * dot(oc, B)
    c = dot(oc, oc) - R*R
    discriminant = b*b - 4*a*c
    if discriminant > 0:
        t1 = (-b - math.sqrt(discriminant)) / (2*a)
        t2 = (-b + math.sqrt(discriminant)) / (2*a)
        t = min(t1, t2)
        return t if t >= 0.0 else None
    return None

def mults(v, s):
    return [v[0]*s, v[1]*s, v[2]*s]

def add(v0, v1):
    return [v0[0]+v1[0], v0[1]+v1[1], v0[2]+v1[2]]

def cross(v0, v1):
    return [
        v0[1]*v1[2]-v1[1]*v0[2],
        v0[2]*v1[0]-v1[2]*v0[0],
        v0[0]*v1[1]-v1[0]*v0[1]]

def PointInOrOn( P1, P2, A, B ):
    CP1 = cross( subtract(B, A), subtract(P1, A) )
    CP2 = cross( subtract(B, A), subtract(P2, A) )
    return dot( CP1, CP2 ) >= 0

def PointInOrOnTriangle( P, A, B, C ):
    return PointInOrOn( P, A, B, C ) and PointInOrOn( P, B, C, A ) and PointInOrOn( P, C, A, B )

# p0, p1   points on ray
# PA, PB, PC  points of the triangle
def isectPlane(p0, p1, PA, PB, PC):
    R0 = p0               # origin 
    D = normalize(subtract(p1, p0))
    P0 = PA
    NV = normalize( cross( subtract(PB, PA), subtract(PC, PA) ) )
    dist_isect = dot( subtract(P0, R0), NV ) / dot( D, NV ) 
    P_isect    = add(R0, mults(D, dist_isect))
    return P_isect, dist_isect

def isectTrianlge(p0, p1, PA, PB, PC):
    P, t = isectPlane(p0, p1, PA, PB, PC)
    if t >= 0 and PointInOrOnTriangle(P, PA, PB, PC):
        return t
    return None

def PointInOrOnQuad( P, A, B, C, D ):
    return (PointInOrOn( P, A, B, C ) and PointInOrOn( P, B, C, D ) and
            PointInOrOn( P, C, D, A ) and PointInOrOn( P, D, A, B ))

def isectQuad(p0, p1, PA, PB, PC, PD):
    P, t = isectPlane(p0, p1, PA, PB, PC)
    if t >= 0 and PointInOrOnQuad(P, PA, PB, PC, PD):
        return t
    return None
    
def isectCuboid(p0, p1, pMin, pMax):
    t = None
    try:
        pl = [[pMin[0], pMin[1], pMin[2]], [pMax[0], pMin[1], pMin[2]],
              [pMax[0], pMax[1], pMin[2]], [pMin[0], pMax[1], pMin[2]],
              [pMin[0], pMin[1], pMax[2]], [pMax[0], pMin[1], pMax[2]],
              [pMax[0], pMax[1], pMax[2]], [pMin[0], pMax[1], pMax[2]]]
        il = [[0, 1, 2, 3], [4, 5, 6, 7], [4, 0, 3, 7], [1, 5, 6, 2], [4, 3, 1, 0], [3, 2, 6, 7]]
        for qi in il:
            ts = isectQuad(p0, p1, pl[qi[0]], pl[qi[1]], pl[qi[2]], pl[qi[3]] )
            if ts != None and ts >= 0 and (t == None or ts < t):
                t = ts
    except:
        t = None
    return t