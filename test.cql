
CREATE KEYSPACE IF NOT EXISTS discussion_forum WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };

DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
  username text,
  password text,
  Primary Key (username, password)
);

DROP TABLE IF EXISTS Content;

CREATE TABLE Content (
  forumid uuid,
  threadid uuid,
  threadtitle text,
  postid uuid,
  postauthor text,
  posttimestamp timestamp,
  posttext text,
  Primary Key (postid)
);

CREATE INDEX ON discussion_forum.Content (threadid);

CREATE INDEX ON discussion_forum.Content (posttimestamp);

DROP TABLE IF EXISTS Forums;

CREATE TABLE Forums (
  forumid uuid,
  forumcreator text,
  forumtitle text,
  Primary Key (forumid)
);

--Users Inserts
INSERT INTO discussion_forum.Users (username, password)
VALUES ('cameron', 'test');

INSERT INTO discussion_forum.Users (username, password)
VALUES ('brian', 'test');

INSERT INTO discussion_forum.Users (username, password)
VALUES ('elmer', 'test');

-- Fourm Inserts
INSERT INTO discussion_forum.Forums (forumid, forumcreator, forumtitle)
VALUES (a5d59ef0-ec41-11e8-81a8-000000000000, 'cameron', 'Forum1');

INSERT INTO discussion_forum.Forums (forumid, forumcreator, forumtitle)
VALUES (a5d61420-ec41-11e8-81a8-000000000000, 'brian', 'Forum2');

INSERT INTO discussion_forum.Forums (forumid, forumcreator, forumtitle)
VALUES (a697b670-ec41-11e8-81a8-000000000000, 'elmer', 'Forum2');

-- Thread Inserts
INSERT INTO discussion_forum.Content (forumid, threadid, threadtitle, postid, postauthor, posttimestamp, posttext)
VALUES (a5d59ef0-ec41-11e8-81a8-000000000000, 420399d1-f804-11e8-9332-000000000000, 'Forum 1, Thread 1', now(), 'cameron', dateof(now()), 'Forum 1, Thread 1, Post 1');

INSERT INTO discussion_forum.Content (forumid, threadid, threadtitle, postid, postauthor, posttimestamp, posttext)
VALUES (a5d59ef0-ec41-11e8-81a8-000000000000, a5d61420-ec41-11e8-81a8-000000000000, 'Forum 1, Thread 2', now(), 'brian', dateof(now()), 'Forum 1, Thread 2, Post 1');

INSERT INTO discussion_forum.Content (forumid, threadid, threadtitle, postid, postauthor, posttimestamp, posttext)
VALUES (a5d61420-ec41-11e8-81a8-000000000000, a5d59ef0-ec41-11e8-81a8-000000000000, 'Forum 2, Thread 1', now(), 'elmer', dateof(now()), 'Forum 2, Thread 1, Post 1');

-- Post Inserts
INSERT INTO discussion_forum.Content (forumid, threadid, postid, postauthor, posttimestamp, posttext)
VALUES (a5d59ef0-ec41-11e8-81a8-000000000000, 420399d1-f804-11e8-9332-000000000000, now(), 'cameron', dateof(now()),'Forum 1, Thread 1, Post 2');

INSERT INTO discussion_forum.Content (forumid, threadid, postid, postauthor, posttimestamp, posttext)
VALUES (a5d59ef0-ec41-11e8-81a8-000000000000, 420399d1-f804-11e8-9332-000000000000, now(), 'elmer', dateof(now()),'Forum 1, Thread 1, Post 3');

INSERT INTO discussion_forum.Content (forumid, threadid, postid, postauthor, posttimestamp, posttext)
VALUES (a5d59ef0-ec41-11e8-81a8-000000000000, a5d61420-ec41-11e8-81a8-000000000000, now(), 'elmer', dateof(now()),'Forum 1, Thread 2, Post 2');