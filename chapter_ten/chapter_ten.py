"""
Created by 陈辰柄 
datetime:2020/4/15 2:38
Describe:自动映射进行反射
"""

from sqlalchemy.ext.automap import automap_base
from sqlalchemy import inspect,insert,create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, func

Base = automap_base()



engine = create_engine('sqlite:///Chinook_Sqlite.sqlite')
mysql_engine = create_engine("mysql+mysqlconnector://root:@localhost:3306/guest", pool_recycle=3600)
Base.prepare(engine, reflect=True)

Base.metadata.create_all(mysql_engine)

Artist = Base.classes.Artist
Album = Base.classes.Album


sqlite_session = Session(engine)
mysql_session = Session(mysql_engine)


def print_state(object):
    insp = inspect(object)
    for state in ['transient', 'pending', 'persistent', 'detached']:
        print('{:>10}: {}'.format(state, getattr(insp, state)))
    print()


nums_sql = select([func.count(Artist.Name)])
select_Sql = select([Artist])

connection = engine.connect()
mysql_connection = mysql_engine.connect()

nums = connection.execute(nums_sql).first().count_1
print(nums)

for i in range(0, nums, 10):
    # select_Sql = select_Sql.slice(i, i + 1000).all()
    select_Sql = select_Sql.offset(i).limit(10)
    results = connection.execute(select_Sql)
    list_results=[tuple(i) for i in results]
    print(list_results)
    ins = insert(Artist).values(list_results)
    mysql_connection.execute(ins)
