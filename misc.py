import os


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
            images.append(tempDict)

    #print(images)
    return images