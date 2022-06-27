from mimetypes import init
from misc import *

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from datetime import datetime
import re
import os


from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, select,func
engine = create_engine('sqlite:///posts.db', echo=True)
meta = MetaData()

posts_details = Table(
   'posts_details', meta, 
   Column('hash', String, primary_key = True),
   Column('path', String),
   Column('class', String),
   Column('title', String),
)

posts_order = Table(
   'posts_order', meta, 
   Column('hash', Integer, ForeignKey('posts_details.hash')), 
   Column('order', Integer),
)



meta.create_all(engine)

conn = engine.connect()
initial_posts = get_all_images()
conn.execute(posts_details.insert(), initial_posts) #populate posts_details
initial_order = []
for i in range(len(initial_posts)):
    tempDict = {}
    tempDict['hash'] = initial_posts[i]['hash']
    tempDict['order'] = i
    initial_order.append(tempDict)
conn.execute(posts_order.insert(), initial_order)




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
    images = []
    conn = engine.connect()
    stmt = select(posts_order.c.hash).order_by(posts_order.c.order)    #selects all hashes
    response = conn.execute(stmt)
    for row in response:
        stmt = posts_details.select().where(posts_details.c.hash == row[0]) #selects details from posts_details based on hash
        new_response = conn.execute(stmt)
        for i in new_response:
            tempDict = {}
            i = i._asdict()
            tempDict['path'] = i['path']
            tempDict['class'] = i['class']
            tempDict['title'] = i['title']
            images.append(tempDict)

    return render_template("gallery.html",images=images)