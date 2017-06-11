import sys
import glob
import os
import numpy as np
from iou_utils import *

path = sys.argv[1]
l = len(path)
if ( path[l-1] != "/" ):
    path += "/"

thres = float(sys.argv[2])

files = glob.glob(path+"*.txt")

for f in files:
    if ( os.path.getsize(f) > 0 ):
        r = np.loadtxt(f)
        try:
            cols = r.shape[1]
            rows = r.shape[0]
            n = np.zeros(shape=(rows, cols))
            i_old = 0
            i_new = 0
            for k in range(0, rows-1):
                x1 = r[k][0]
                y1 = r[k][1]
                x2 = r[k][2]
                y2 = r[k][3]
                s1 = r[k][4]
                for l in range(k+1, rows):
                    x3 = r[l][0]
                    y3 = r[l][1]
                    x4 = r[l][2]
                    y4 = r[l][3]
                    s2 = r[l][4]
                    iou = find_iou(x1, y1, x2, y2, x3, y3, x4, y4)
                    if ( iou >= thres ):
                        x5, y5, x6, y6, s = find_new_coords_score(x1, y1, x2, y2, x3, y3, x4, y4, s1, s2)
                        n[i_new][0] = x5
                        n[i_new][1] = y5
                        n[i_new][2] = x6
                        n[i_new][3] = y6
                        n[i_new][4] = s
                        r[k][0] = 1
                        r[k][1] = 1
                        r[k][2] = 1
                        r[k][3] = 1
                        r[l][0] = 1
                        r[l][1] = 1
                        r[l][2] = 1
                        r[l][3] = 1
                        i_new += 1
                        l = rows
                if ( i_new == i_old ):
                    n[i_new][0] = r[k][0]
                    n[i_new][1] = r[k][1]
                    n[i_new][2] = r[k][2]
                    n[i_new][3] = r[k][3]
                    n[i_new][4] = r[k][4]
                    i_new += 1
                i_old = i_new
            if ( r[rows-1][0]!=1 and r[rows-1][1]!=1 and r[rows-1][2]!=1 and r[rows-1][3]!=1 ):
                n[i_new][0] = r[rows-1][0]
                n[i_new][1] = r[rows-1][1]
                n[i_new][2] = r[rows-1][2]
                n[i_new][3] = r[rows-1][3]
                n[i_new][4] = r[rows-1][4]
                i_new += 1
                i_old = i_new
            nn = n[np.ix_(range(0,i_old), range(0,cols))]
            np.savetxt(f, nn, '%d %d %d %d %f')
        except IndexError:
            continue
