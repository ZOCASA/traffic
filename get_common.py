import sys
import glob
import os
import numpy as np
from iou_utils import *

path = sys.argv[1]
l = len(path)
if ( path[l-1] != "/" ):
    path += "/"

folder1 = sys.argv[2]
folder2 = sys.argv[3]

thres = float(sys.argv[4])

files1 = glob.glob(path+folder1+"/*.txt")
files2 = glob.glob(path+folder2+"/*.txt")

for f1 in files1:
    for f2 in files2:
        if (os.path.basename(f1) == os.path.basename(f2)):
            if ( os.path.getsize(f1) > 0 and os.path.getsize(f2) > 0 ):
                os.system('cat '+f1+' '+f2+' > temp.txt')
                r = np.loadtxt('temp.txt')
                try:
                    cols = r.shape[1]
                    rows = r.shape[0]
                    n = np.zeros(shape=(rows, cols))
                    i = 0
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
                                n[i][0] = x5
                                n[i][1] = y5
                                n[i][2] = x6
                                n[i][3] = y6
                                n[i][4] = s
                                r[k][0] = 1
                                r[k][1] = 1
                                r[k][2] = 1
                                r[k][3] = 1
                                r[l][0] = 1
                                r[l][1] = 1
                                r[l][2] = 1
                                r[l][3] = 1
                                i += 1
                                l = rows
                    f = path+os.path.basename(f1)
                    nn = n[np.ix_(range(0,i), range(0,cols))]
                    np.savetxt(f, nn, '%d %d %d %d %f')
                except IndexError:
                    continue
