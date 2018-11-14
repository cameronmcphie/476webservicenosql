
DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
  username text,
  password text,
  Primary Key (username, password)
);
DROP TABLE IF EXISTS Content;
CREATE TABLE Content (
    forumid int,
    threadid int,
    forumcreator text,
    forumtitle text,
    threadtitle text,
    postauthor text,
    posttimestamp timestamp,
    posttext text,
    Primary Key (forumid, threadid, posttimestamp)
);

--DROP KEYSPACE IF EXISTS discussion_forum;

--CREATE KEYSPACE IF NOT EXISTS discussion_forum
--WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
--CREATE INDEX ON discussion_forum.Content (threadId);

--CREATE INDEX ON discussion_forum.Content (postTimestamp);

--INSERT INTO discussion_forum.Content ()