import sys
import os, os.path
import glob
import numpy as np
from PIL import Image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras.callbacks import ModelCheckpoint
from keras import applications

# dimensions of our images.
img_width, img_height = 150, 150

input_data_dir = sys.argv[1]
ext = sys.argv[2]
nb_input_data = 20
#nb_input_data = len([name for name in os.listdir(input_data_dir) if os.path.isfile(os.path.join(input_data_dir, name))])
#print(str(nb_input_data))
#batch_size = 16
batch_size = 10


orig = os.getcwd()
os.chdir(input_data_dir+'../segmented/')
dest = os.getcwd()
os.chdir(orig)


def get_bottlebeck_features():
    datagen = ImageDataGenerator(rescale=1. / 255)

    # build the VGG16 network
    model = applications.VGG16(include_top=False, weights='imagenet')

    bottleneck_features = model.predict(
        input_data,
        batch_size=batch_size)

    return bottleneck_features


def get_predictions(features):
    model = Sequential()
    model.add(Flatten(input_shape=features.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='rmsprop',
        loss='binary_crossentropy', metrics=['accuracy'])

    filepath = "weights-best.hdf5"
    model.load_weights(filepath)

    predictions = model.predict_classes(features,
        batch_size=batch_size)

    return predictions


folders = glob.glob(input_data_dir+"*")
for fd in folders:
    files = glob.glob(fd+"/*."+ext)
    cntr = 0
    for f in files:
        im = Image.open(f)
        im = im.resize((img_width, img_height), Image.NEAREST)
        if (im.mode == 'L'):
            im = im.convert('RGB')
        input_data = np.array(im)
        input_data = np.divide(input_data, 255.0)
        input_data = np.expand_dims(input_data, 0)
        features = get_bottlebeck_features()
        classes = get_predictions( features )
        if (classes[0] == 0):
            print(f+': Detected')
            cntr = 1
            break
        else:
            print(f+': Not detected')
    if (cntr != 0):
        f = dest+'/'+ os.path.basename(fd)
        os.system('python3 alpr_image.py '+f+'.'+ext)
