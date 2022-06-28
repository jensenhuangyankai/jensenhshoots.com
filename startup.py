from misc import *
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, select,func,intersect,delete

"""FILE contains all the database information that is executed on every startup"""



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


def image_check(conn):
    """checking if any files were removed but the database wasnt informed"""
    initial_posts = get_all_images()
    initial_hashes = []
    for i in initial_posts:
        initial_hashes.append({'hash' : i['hash']})
    stmt = select(posts_details.c.hash)
    response = conn.execute(stmt).mappings().all() #returns a list of dictionaries [{'hash':value},{'hash':value}]
    for i in response:
        if i not in initial_hashes:
            stmt = delete(posts_details).where(posts_details.c.hash == i['hash'])
            conn.execute(stmt)

def populate_db(conn):
    """POPULATING posts_details on startup"""      
    initial_posts = get_all_images()
    for i in initial_posts:
        stmt = select(posts_details.c.hash)
        response = conn.execute(stmt).mappings().all() #returns a list of dictionaries [{'hash':value},{'hash':value}]
        if {'hash':i['hash']} not in response:
            print({'hash':i['hash']})
            conn.execute(posts_details.insert(), i) #populate posts_details

    """POPULATING posts_order on startup"""       
    stmt = intersect(select(posts_details.c.hash),select(posts_order.c.hash)) #select if both tables have hash value
    hashlist = conn.execute(stmt).mappings().all() #returns a list of dictionaries [{'hash':value},{'hash':value}]
    for i in range(len(initial_posts)):
        tempDict = {}
        tempDict['hash'] = initial_posts[i]['hash']
        if tempDict in hashlist:
            pass
        else:
            tempDict['order'] = i
            print(tempDict)
            conn.execute(posts_order.insert(), [tempDict])

def start():
    meta.create_all(engine)
    conn = engine.connect()
    image_check(conn)
    populate_db(conn)