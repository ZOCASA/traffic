"""
draws license plate regions onto input image
python scriptname filename

TODO: get arguments for OpenALPR
"""

import sys
import os
import json
import numpy as np
import cv2
import random
from PIL import Image
import glob
import shutil

blankStr = '                                                  '
jsonOutputFile = 'plateCoordinates.txt'

inputPath, imageFile = os.path.split(sys.argv[1])

filename = inputPath+'/'+imageFile

# alpr for frames
os.system('alpr -c in -j '+filename.replace(' ', '\ ')+' > '+jsonOutputFile)

# file containing JSON results from OpenALPR
with open(jsonOutputFile) as jsonFile:
    jsonData = json.load(jsonFile)
    jsonFile.close()

    # fetching results from the JSON
    results = jsonData['results']
    numPlates = len(results)

    # opening image onto which license plates are to be shown
    img = cv2.imread(filename, 1)

    if numPlates > 0:
        # for all plates get the result and
        # coordinates for bounding box.
        i = 0
        for plate in results:
            coords = plate['coordinates']
            detectedNumber = plate['plate']
            topLeft = coords[0]
            bottomRight = coords[2]

            # coordinate for license plate boundong box
            x1 = topLeft ['x']
            y1 = topLeft ['y']
            x2 = bottomRight['x']
            y2 = bottomRight['y']

            # font settings
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 2
            text = 'plate '+str(i)
            text = detectedNumber
            textThickness = 5

            # other parameters
            boxThickness = 10
            shift = 4

            # size of text box
            size, baseLine = cv2.getTextSize(text, font, fontScale, textThickness)

            # coordinates for text box
            x3 = x1-shift
            y3 = y1-baseLine-size[1]
            x4 = x1-shift+size[0]
            y4 = y1

            # coordinates for text
            x5 = x1+2
            y5 = y1-baseLine+4

            # box color
            bBox = random.randint(0, 200)
            gBox = random.randint(0, 200)
            rBox = random.randint(0, 200)

            # text color
            bText = 255
            gText = 255
            rText = 255

            # plotting rectangle and text
            img = cv2.rectangle(img, (x1, y1), (x2, y2), (bBox, gBox, rBox), boxThickness)
            img = cv2.rectangle(img, (x3, y3), (x4, y4), (bBox, gBox, rBox), -1)
            img = cv2.putText(img, text, (x5, y5), font, fontScale, (bText, gText, rText), textThickness, cv2.LINE_AA)

            i += 1

    # saving image
    cv2.imwrite(os.path.splitext(os.path.basename(filename))[0]+'_alpr_out.jpg', img);

    # displaying image
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 1280, 720)
    cv2.imshow('image', img)
    cv2.waitKey(2000)

os.remove(jsonOutputFile)
