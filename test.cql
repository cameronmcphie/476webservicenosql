
--CREATE KEYSPACE IF NOT EXISTS discussion_forum WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };

DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
  username text,
  password text,
  Primary Key (username, password)
);

DROP TABLE IF EXISTS Content;

CREATE TABLE Content (
    forumid uuid,
    forumcreator text,
    forumtitle text,
    threadid uuid,
    threadtitle text,
    postid uuid,
    postauthor text,
    posttimestamp timestamp,
    posttext text,
    Primary Key (postid)
);

CREATE INDEX ON discussion_forum.Content (forumid);

CREATE INDEX ON discussion_forum.Content (threadid);

CREATE INDEX ON discussion_forum.Content (posttimestamp);

--Users Inserts
INSERT INTO discussion_forum.Users (username, password)
VALUES ('cameron', 'test');

INSERT INTO discussion_forum.Users (username, password)
VALUES ('brian', 'test');

INSERT INTO discussion_forum.Users (username, password)
VALUES ('elmer', 'test');

-- Fourm Inserts
-- INSERT INTO discussion_forum.Content (forumid, forumcreator, forumtitle) 
-- VALUES (now(), 'cameron', 'Forum1');

INSERT INTO discussion_forum.Content (forumid, forumcreator, forumtitle, postid) 
VALUES (a5d59ef0-ec41-11e8-81a8-000000000000, 'cameron', 'Forum1', now());

INSERT INTO discussion_forum.Content (forumid, forumcreator, forumtitle, postid) 
VALUES (a5d61420-ec41-11e8-81a8-000000000000, 'brian', 'Forum2', now());

INSERT INTO discussion_forum.Content (forumid, forumcreator, forumtitle, postid) 
VALUES (a697b670-ec41-11e8-81a8-000000000000, 'elmer', 'Forum2', now());

-- Thread Inserts
INSERT INTO discussion_forum.Content (forumid, threadid, threadtitle, postid, postauthor, posttimestamp, posttext)
VALUES (a5d59ef0-ec41-11e8-81a8-000000000000, now(), 'Forum 1, Thread 1', now(), 'cameron', dateof(now()), 'Post text 1');

INSERT INTO discussion_forum.Content (forumid, threadid, threadtitle, postid, postauthor, posttimestamp, posttext)
VALUES (a5d59ef0-ec41-11e8-81a8-000000000000, now(), 'Forum 1, Thread 2', now(), 'brian', dateof(now()), 'Post text 2');

INSERT INTO discussion_forum.Content (forumid, threadid, threadtitle, postid, postauthor, posttimestamp, posttext)
VALUES (a5d61420-ec41-11e8-81a8-000000000000, now(), 'Forum 2, Thread 3', now(), 'elmer', dateof(now()), 'Post text 3');

-- Post Inserts
INSERT INTO discussion_forum.Content (forumid, threadid, threadtitle, postid, postauthor, posttimestamp, posttext)
VALUES 