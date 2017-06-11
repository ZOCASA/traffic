def check_overlap(x1, y1, x2, y2, x3, y3, x4, y4):
    if ( x3>=x2 or x1>=x4 or y3>=y2 or y1>= y4 ):
        return 0
    return 1

def find_new_coords_score(x1, y1, x2, y2, x3, y3, x4, y4, s1, s2):
    if ( check_overlap(x1, y1, x2, y2, x3, y3, x4, y4) == 1 ):
        x5 = max(x1, x3)
        y5 = max(y1, y3)
        x6 = min(x2, x4)
        y6 = min(y2, y4)
        s = (s1+s2)/2
        return x5, y5, x6, y6, s

def find_union(x1, y1, x2, y2, x3, y3, x4, y4):
    if ( check_overlap(x1, y1, x2, y2, x3, y3, x4, y4) == 1 ):
        intersect = find_intersection(x1, y1, x2, y2, x3, y3, x4, y4)
        a1 = (x2-x1) * (y2-y1)
        a2 = (x4-x3) * (y4-y3)
        area = a1 + a2 - intersect
        return area
    else:
        return 0

def find_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    if ( check_overlap(x1, y1, x2, y2, x3, y3, x4, y4) == 1 ):
        x5, y5, x6, y6, s = find_new_coords_score(x1, y1, x2, y2, x3, y3, x4, y4, 0, 0)
        area = (x6-x5) * (y6-y5)
        return area
    else:
        return 0

def find_iou(x1, y1, x2, y2, x3, y3, x4, y4):
    if ( check_overlap(x1, y1, x2, y2, x3, y3, x4, y4) == 1 ):
        intersect = find_intersection(x1, y1, x2, y2, x3, y3, x4, y4)
        union = find_union(x1, y1, x2, y2, x3, y3, x4, y4)
        iou = float(intersect)/float(union)
        return iou
    else:
        return 0
