import os
import sys

path = sys.argv[1]
ext = sys.argv[2]

############################# SSD #################################
owd = os.getcwd()
os.chdir(owd+'/caffe/examples/')

os.system('python test.py '+path+' '+ext)

os.chdir(owd)

print('SSD finished')
###################################################################


############################# remove duplicates ###################
path_temp = path + 'ssd/'
os.system('python rm_dups.py '+path_temp+' 0.3')

path_temp = path + 'yolo/'
os.system('python rm_dups.py '+path_temp+' 0.3')

print('duplicates removed')
###################################################################


############################# combine regions and segment #########
os.system('python get_common.py '+path+' ssd yolo 0.2')

os.system('python3 segment.py '+path+' '+ext)

print('regions combined and segmented')
###################################################################


############################# roi for helmet ######################
os.system('python3 helmetROI.py '+path+' '+ext)

print('helemt roi generated')
###################################################################


############################# helmet detection and lpd ############
path_temp = path + 'helmet/'
os.system('python prdct.py '+path_temp+' '+ext)

print('helmet detection and lpd completed')
###################################################################
