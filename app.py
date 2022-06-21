from flask import Flask, flash, jsonify, redirect, render_template, request, session
from datetime import datetime
import re
import os

app = Flask(__name__)

@app.route("/")
def index():
    carouselPaths = []
    carouselNames = []
    carouselFolders = [x[0] for x in os.walk("static/Images")][1:] #finds the number of carousel folders in static/Images
    #print(carouselFolders)
    for folder in carouselFolders: 
        photos = []
        carouselNames.append(folder.replace('static/Images/',''))
        for file in os.listdir(folder):
            filename =  folder + "/" + file 
            photos.append(filename)
        carouselPaths.append(photos)

    carouselPaths = carouselPaths[::-1] 
    carouselNames = carouselNames[::-1]
    """##################################################################"""
    """                                                                  """
    """ FOR FUTURE DOCUMENTATION YOU REVERSED THIS THING FOR SOME REASON """
    """                                                                  """
    """##################################################################"""
    return render_template("index.html", carousels = carouselPaths, names = carouselNames)

@app.route("/gallery")
def gallery():

    filenames = next(os.walk("static/Images"), (None, None, []))[2]  # [] if no file
    #print(filenames)
    newlist = []
    extensions = []
    for k in filenames:
        newlist.append(os.path.splitext(k)[0])
        extensions.append(os.path.splitext(k)[1])

    #for i in range(len(newlist)):
        #print("\'" + newlist[i].split()[0] + "\'")

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
    return render_template("gallery.html",images=images)