import numpy as np
import os
import cv2
import sys
import glob

path = sys.argv[1]
l = len(path)
if (path[l-1] != '/'):
    path += '/'

ext = sys.argv[2]
ext = '.' + ext

out_path = path+'segmented/'

if not os.path.exists(out_path):
    os.makedirs(out_path)

files = glob.glob(path+'*.txt')

for f in files:
    if (os.path.getsize(f) > 0):
        name = os.path.basename(f).split('.')[0]
        r = np.loadtxt(f)
        i = os.path.splitext(f)[0]+ext
        img = cv2.imread(i)
        try:
            cols = r.shape[1]
            rows = r.shape[0]
            for k in range(0, rows):
                x1 = int(r[k][0])
                y1 = int(r[k][1])
                x2 = int(r[k][2])
                y2 = int(r[k][3])
                crop = img[y1:y2, x1:x2, :]
                #cv2.namedWindow('image', cv2.WINDOW_NORMAL)
                #cv2.resizeWindow('image', 800, 800)
                #cv2.imshow('image', crop)
                #cv2.waitKey(2000)
                out = out_path+name+'_'+str(k)+ext
                cv2.imwrite(out, crop)
        except IndexError:
            crop = img[int(r[1]):int(r[3]), int(r[0]):int(r[2])]
            out = out_path+name+'_0'+ext
            cv2.imwrite(out, crop)
