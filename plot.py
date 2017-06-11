import numpy as np
import cv2
import glob
import os
from os.path import basename
import sys

path = sys.argv[1]
ext = sys.argv[2]
path_txt = sys.argv[3]

l = len(path)
if (path[l-1] != '/'):
    path += "/"

l = len(path_txt)
if (path_txt[l-1] != '/'):
    path_txt += "/"

files = glob.glob(path+'*.'+ext)

for f in files:
    name = basename(f).split(".")[0]
    print(f)
    img = cv2.imread(f, 1)
    roiFile = open(path_txt+name+'.txt', 'r')
    lines = roiFile.readlines()
    numLines = len(lines)
    for k in range(0, numLines):
        line = lines[k]
        e = line.split()
        xmin = int(e[0])
        ymin = int(e[1])
        xmax = int(e[2])
        ymax = int(e[3])
        score = float(e[4])
        img = cv2.rectangle(img, (xmin,ymin), (xmax,ymax), (255,255,255), 10)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 800, 800)
    cv2.imshow('image', img)
    cv2.waitKey()
    roiFile.close






