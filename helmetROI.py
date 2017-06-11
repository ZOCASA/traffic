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

out_path_main = path+'helmet/'

if not os.path.exists(out_path_main):
    os.makedirs(out_path_main)

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
                out_path = out_path_main+name+'_'+str(k)+'/'
                if not os.path.exists(out_path):
                    os.makedirs(out_path)
                x1 = int(r[k][0])
                y1 = int(r[k][1])
                x2 = int(r[k][2])
                y2 = int(r[k][3])

                w = x2 - x1
                h = y2 - y1
                h = int(h*1.1)

                rem = int(w*0.1)
                x3 = x1 + rem
                y3 = y1 - h
                x4 = x2 - rem
                y4 = y1

                xmid = int((x4-x3)/2)
                ymid = int((y4-y3)/2)

                #1
                y5 = y3
                y6 = y3 + ymid
                if (y5 < 1):
                    y5 = 1
                if (y6 > y5):
                    crop = img[y5:y6, x3:x4, :]
                    out = out_path+'1'+ext
                    cv2.imwrite(out, crop)
                #2
                y5 = y3 + ymid + 1
                y6 = y4
                if (y5 < 1):
                    y5 = 1
                if (y6 > y5):
                    crop = img[y5:y6, x3:x4, :]
                    out = out_path+'2'+ext
                    cv2.imwrite(out, crop)
                #3
                y5 = y3 + int(h/4)
                y6 = y4 - int(h/4)
                if (y5 < 1):
                    y5 = 1
                if (y6 > y5):
                    crop = img[y5:y6, x3:x4, :]
                    out = out_path+'3'+ext
                    cv2.imwrite(out, crop)

                #cv2.namedWindow('image', cv2.WINDOW_NORMAL)
                #cv2.resizeWindow('image', 800, 800)
                #cv2.imshow('image', crop)
                #cv2.waitKey(2000)
        except IndexError:
            out_path = out_path_main+name+'_0/'
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            x1 = int(r[0])
            y1 = int(r[1])
            x2 = int(r[2])
            y2 = int(r[3])

            w = x2 - x1
            h = y2 - y1
            h = int(h*1.1)

            rem = int(w*0.1)
            x3 = x1 + rem
            y3 = y1 - h
            x4 = x2 - rem
            y4 = y1

            xmid = int((x4-x3)/2)
            ymid = int((y4-y3)/2)

            #1
            y5 = y3
            y6 = y3 + ymid
            if (y5 < 1):
                y5 = 1
            if (y6 > y5):
                crop = img[y5:y6, x3:x4, :]
                out = out_path+'1'+ext
                cv2.imwrite(out, crop)
            #2
            y5 = y3 + ymid + 1
            y6 = y4
            if (y5 < 1):
                y5 = 1
            if (y6 > y5):
                crop = img[y5:y6, x3:x4, :]
                out = out_path+'2'+ext
                cv2.imwrite(out, crop)
            #3
            y5 = y3 + int(h/4)
            y6 = y4 - int(h/4)
            if (y5 < 1):
                y5 = 1
            if (y6 > y5):
                crop = img[y5:y6, x3:x4, :]
                out = out_path+'3'+ext
                cv2.imwrite(out, crop)
