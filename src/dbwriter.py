import os
import random

from shutil import copyfile

folders = os.listdir('../dataset/augmented')

if folders[0] == ".DS_Store":
    del folders[0]

    # create files and directories
f = open('../dataset/words.txt', 'w+')
if not os.path.exists('../dataset/sub'):
    os.makedirs('../dataset/sub')
if not os.path.exists('../dataset/sub/sub-sub'):
    os.makedirs('../dataset/sub/sub-sub')

counter=1
threshold=10

for folder in folders:
    if folder !=".DS_Store" :
        images = os.listdir('../dataset/augmented/' + folder)
        if images[0] == ".DS_Store":
            del images[0]
        files = os.listdir('../dataset/segmented/' + folder)
        if len(files)> threshold:
            print("saving: " + folder)
            for image in images:
                imageName= "sub-sub-"+str(counter) +".png"
                savingDir = ("../dataset/sub/sub-sub/" + imageName )
                imagesDir = ("../dataset/augmented/" + folder + "/" + image)
                copyfile(imagesDir, savingDir)
                line = imageName+ ' X X X X X X X ' + folder + '\n'
                f.write(line)
                counter+=1


f.close()
os.system('python shuffle.py words.txt')
