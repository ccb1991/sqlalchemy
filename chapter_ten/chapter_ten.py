"""
Created by 陈辰柄 
datetime:2020/4/15 2:38
Describe:自动映射进行反射
"""

from sqlalchemy.ext.automap import automap_base

Base = automap_base()

from sqlalchemy import create_engine

engine = create_engine('sqlite:///Chinook_Sqlite.sqlite')

Base.prepare(engine, reflect=True)

print(Base.classes.keys())

Artist = Base.classes.Artist
Album = Base.classes.Album

from sqlalchemy.orm import Session

session=Session(engine)
for artist in session.query(Artist).limit(10):
    print(artist.ArtistId,artist.Name)
