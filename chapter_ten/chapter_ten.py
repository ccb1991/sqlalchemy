"""
Created by 陈辰柄 
datetime:2020/4/15 2:38
Describe:自动映射进行反射
"""

from sqlalchemy.ext.automap import automap_base

Base = automap_base()

from sqlalchemy import create_engine
from sqlalchemy.sql import select

engine = create_engine('sqlite:///Chinook_Sqlite.sqlite')
mysql_engine = create_engine("mysql+mysqlconnector://root:@localhost:3306/guest", pool_recycle=3600)
Base.prepare(engine, reflect=True)

Base.metadata.create_all(mysql_engine)
print(Base.classes.keys())

Artist = Base.classes.Artist
Album = Base.classes.Album

from sqlalchemy.orm import Session

sqllite_session = Session(engine)
nums = sqllite_session.query(Artist).count()

mysql_session = Session(mysql_engine)
result1=mysql_session.query(Artist).first()
print(result1.Name,result1.ArtistId)
for i in range(0, nums, 100):
    result = sqllite_session.query(Artist).slice(i, i + 100).all()
    for j in result:
        sqllite_session.expunge(j)
        # print(j.Name)
        mysql_session.add(j)
        mysql_session.commit()
    # try:
    #     mysql_session.commit()
    # except:
    #     print("error")
    #     mysql_session.rollback()
