from flask import Flask
from helper_funs import get_db

from cassandra.cluster import Cluster
from datetime import datetime
from uuid import UUID
from cassandra import util

app = Flask(__name__)
app.config["DEBUG"] = True


@app.cli.command('init_db')
def init_db():
    with app.app_context():


        # possible solution to use https://stackoverflow.com/questions/49863780/execute-cql-queries-from-file-using-the-datastax-python-cassandra-driver
        # http://datastax.github.io/python-driver/lwt.html
        # http://datastax.github.io/python-driver/api/cassandra/auth.html
        # https://www.researchgate.net/post/Populating_Cassandra_database_using_Python


        cluster = Cluster(['172.17.0.1 ','172.17.0.2'])

        session = cluster.connect() #keyspace optional

        # db = get_db()

        # with app.open_resource('init.sql', mode='r') as f:
        #     #db.cursor().executescript(f.read())
        #
        # #db.commit()

        # with app.open_resource('test.cql', mode='r') as f: #untested
        #     session.execute(f.read())

        session.execute("CREATE KEYSPACE IF NOT EXISTS discussion_forum WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };")

        session.execute("USE discussion_forum;")

        session.execute("DROP TABLE IF EXISTS Users;")

        session.execute("""CREATE TABLE Users (
          username text,
          password text,
          Primary Key (username)
        );""")

        session.execute("DROP TABLE IF EXISTS Content;")

        session.execute("""
            CREATE TABLE Content (
                  forumid uuid,
                  threadid uuid,
                  threadtitle text,
                  postid uuid,
                  postauthor text,
                  posttimestamp timestamp,
                  posttext text,
                  mostrecenttimestamp timestamp,
                  Primary Key (postid)
                );
        """)
        
        session.execute("CREATE INDEX ON discussion_forum.Content (forumid);")

        session.execute("CREATE INDEX ON discussion_forum.Content (threadid);")

        # session.execute("CREATE INDEX ON discussion_forum.Content (postid);")

        session.execute("CREATE INDEX ON discussion_forum.Content (posttimestamp);")

        session.execute("DROP TABLE IF EXISTS Forums;")

        session.execute("""CREATE TABLE Forums (
          forumid uuid,
          forumcreator text,
          forumtitle text,
          Primary Key (forumid)
        );""")

        session.execute("CREATE INDEX on discussion_forum.Forums (forumtitle);")

        session.execute("""
        INSERT INTO discussion_forum.Users (username, password)
        VALUES (%s, %s);
        """, ('cameron', 'test'))

        session.execute("""
        INSERT INTO discussion_forum.Users (username, password)
        VALUES (%s, %s);
        """, ('brian', 'test'))

        session.execute("""
        INSERT INTO discussion_forum.Users (username, password)
        VALUES (%s, %s);
        """, ('elmer', 'test'))

        #insert test data for the discussion forums (forums)
        session.execute("""
        INSERT INTO discussion_forum.Forums (forumid, forumcreator, forumtitle)
        VALUES (%s, %s, %s);
        """,(UUID('a5d59ef0-ec41-11e8-81a8-000000000000'), 'cameron', 'Forum1'))

        session.execute("""
        INSERT INTO discussion_forum.Forums (forumid, forumcreator, forumtitle)
        VALUES (%s,%s,%s);
        """,(UUID('a5d61420-ec41-11e8-81a8-000000000000'), 'brian', 'Forum2'))

        session.execute("""
        INSERT INTO discussion_forum.Forums (forumid, forumcreator, forumtitle)
        VALUES (%s,%s,%s);
        """,(UUID('a697b670-ec41-11e8-81a8-000000000000'), 'elmer', 'Forum2'))

        #insert test data for threads
        session.execute("""
        INSERT INTO discussion_forum.Content (forumid, threadid, threadtitle, postid, postauthor, posttimestamp, posttext, mostrecenttimestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """,(UUID('a5d59ef0-ec41-11e8-81a8-000000000000'),UUID('420399d1-f804-11e8-9332-000000000000'), 'Forum 1, Thread 1', util.uuid_from_time(datetime.utcnow()), 'cameron', datetime.utcnow(), 'Post text 1', datetime.utcnow()))
                                                                                                                                    #used to be dateof(datetime.utcnow())
        session.execute("""
        INSERT INTO discussion_forum.Content (forumid, threadid, threadtitle, postid, postauthor, posttimestamp, posttext, mostrecenttimestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """,(UUID('a5d59ef0-ec41-11e8-81a8-000000000000'), UUID('a5d61420-ec41-11e8-81a8-000000000000'), 'Forum 1, Thread 2', util.uuid_from_time(datetime.utcnow()), 'brian', datetime.utcnow(), 'Post text 2', datetime.utcnow()))

        session.execute("""
        INSERT INTO discussion_forum.Content (forumid, threadid, threadtitle, postid, postauthor, posttimestamp, posttext, mostrecenttimestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """,(UUID('a5d61420-ec41-11e8-81a8-000000000000'), UUID('a5d59ef0-ec41-11e8-81a8-000000000000'), 'Forum 2, Thread 3', util.uuid_from_time(datetime.utcnow()), 'elmer', datetime.utcnow(), 'Post text 3', datetime.utcnow()))

        #insert test data for posts
        session.execute("""
        INSERT INTO discussion_forum.Content (forumid, threadid, postid, postauthor, posttimestamp, posttext, mostrecenttimestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """,(UUID('a5d59ef0-ec41-11e8-81a8-000000000000'), UUID('420399d1-f804-11e8-9332-000000000000'), util.uuid_from_time(datetime.utcnow()), 'cameron', datetime.utcnow(), 'Forum 1, Thread 1, Post 2', datetime.utcnow()))

        session.execute("""
        INSERT INTO discussion_forum.Content (forumid, threadid, postid, postauthor, posttimestamp, posttext, mostrecenttimestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """,(UUID('a5d59ef0-ec41-11e8-81a8-000000000000'), UUID('420399d1-f804-11e8-9332-000000000000'), util.uuid_from_time(datetime.utcnow()), 'elmer', datetime.utcnow(), 'Forum 1, Thread 1, Post 3', datetime.utcnow()))

        session.execute("""
        INSERT INTO discussion_forum.Content (forumid, threadid, postid, postauthor, posttimestamp, posttext, mostrecenttimestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """,(UUID('a5d59ef0-ec41-11e8-81a8-000000000000'), UUID('a5d61420-ec41-11e8-81a8-000000000000'), util.uuid_from_time(datetime.utcnow()), 'elmer', datetime.utcnow(), 'Forum 1, Thread 2, Post 2', datetime.utcnow()))

    print ('Database Initilaized')

if __name__ == "__main__":
    app.run()
