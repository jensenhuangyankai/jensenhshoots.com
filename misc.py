import os
import sys
import hashlib


def get_all_images():
    filenames = next(os.walk("static/Images"), (None, None, []))[2]  # [] if no file
    #print(filenames)
    newlist = []
    extensions = []
    for k in filenames:
        newlist.append(os.path.splitext(k)[0])
        extensions.append(os.path.splitext(k)[1])

    images = []
    for i in range(len(filenames)):
        if extensions[i] == ".jpg" or extensions[i] == ".jpeg": #or extensions[i] == ".png":
            tempDict = {}
            filename = filenames[i]
            classname = newlist[i].split()[0]
            altname = newlist[i]
            tempDict['path'] = "static/Images/" + filename
            tempDict['class'] = classname
            tempDict['title'] = altname
            tempDict['hash'] = hash(tempDict['path'])
            images.append(tempDict)

    #print(images)
    return images



# BUF_SIZE is totally arbitrary, change for your app!
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
def hash(path):

    sha1 = hashlib.sha1()

    with open(path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)

    #print(sha1.hexdigest())
    return sha1.hexdigest()

