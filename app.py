from misc import *

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from datetime import datetime
import re
import os


from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
engine = create_engine('sqlite:///posts.db', echo=True)
meta = MetaData()

posts_details = Table(
   'posts_details', meta, 
   Column('post_id', Integer, primary_key = True), 
   Column('path', String),
   Column('class', String),
   Column('title', String),
)

posts_order = Table(
   'posts_order', meta, 
   Column('photo_id', Integer, ForeignKey('posts_details.post_id')), 
   Column('order', Integer),
)



meta.create_all(engine)

conn = engine.connect()
initial_posts = get_all_images()
conn.execute(posts_details.insert(), initial_posts)
for i in range(len(initial_posts)):
    conn.execute(posts_order.insert(), [i])



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
    
    
    return render_template("gallery.html",images=images)